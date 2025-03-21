import logging
import typing
from os import environ

import attrs
import pyarrow
import ray
from ray.dag import DAGNode
from ray.dag import MultiOutputNode

from tecton_core import conf
from tecton_core.errors import TectonInternalError
from tecton_core.query.node_interface import EmptyPartition
from tecton_core.query.node_interface import Partitioning
from tecton_core.query.node_interface import PartitionSelector


logger = logging.getLogger(__name__)

PROPAGATE_ENV_VARS = (
    "API_SERVICE",
    "TECTON_API_KEY",
    "DUCKDB_EXTENSION_REPO",
    "SNOWFLAKE_USER",
    "SNOWFLAKE_PASSWORD",
    "REDSHIFT_USER",
    "REDSHIFT_PASSWORD",
    "GOOGLE_APPLICATION_CREDENTIALS",
    "OVERRIDE_CUSTOM_MODEL_PATHS",
)


def _get_runtime() -> typing.Dict[str, typing.Any]:
    env_vars = {}
    for var in PROPAGATE_ENV_VARS:
        try:
            val = conf.get_or_none(var)
        except TectonInternalError:
            val = environ.get(var)

        if not val:
            continue
        env_vars[var] = val

    if conf.get_bool("TECTON_DEBUG"):
        logger.warning(f"Configuring Env vars for Ray tasks: {env_vars}")

    return {"env_vars": env_vars}


@ray.remote
def _write_fragments(input_: pyarrow.Table, partition_key: str, target_partitions: int) -> typing.List[pyarrow.Table]:
    partition_column = input_[partition_key]
    partition_selector = [[] for _ in range(target_partitions)]
    for row_idx, partition_value in enumerate(partition_column.to_pylist()):
        partition_selector[partition_value].append(row_idx)

    return [input_.take(indexes) if indexes else input_.schema.empty_table() for indexes in partition_selector]


@ray.remote
def _read_fragments(*inputs: typing.List[pyarrow.Table]) -> pyarrow.Table:
    return pyarrow.concat_tables(inputs).combine_chunks()


@attrs.define
class RayDataset:
    partitions: typing.List[DAGNode]
    partitioning: Partitioning

    @classmethod
    def from_partition_generator(
        cls, fun: typing.Callable[[PartitionSelector], pyarrow.Table], partitioning: Partitioning
    ) -> "RayDataset":
        partitions = []
        for p in range(partitioning.number_of_partitions):
            partitions.append(ray.remote(fun).options(runtime_env=_get_runtime()).bind(PartitionSelector([p])))

        return cls(partitions, partitioning)

    def map(self, fun: typing.Callable[[pyarrow.Table], pyarrow.Table]) -> "RayDataset":
        output_partitions = []
        for input_partition in self.partitions:
            output_partitions.append(ray.remote(fun).options(runtime_env=_get_runtime()).bind(input_partition))

        return RayDataset(output_partitions, self.partitioning)

    def repartition_by(self, new_partitioning: Partitioning, partition_column: str) -> "RayDataset":
        fragments = []
        for input_partition in self.partitions:
            fragments.append(
                _write_fragments.options(
                    num_returns=new_partitioning.number_of_partitions, runtime_env=_get_runtime()
                ).bind(input_partition, partition_column, new_partitioning.number_of_partitions)
            )

        fragments = MultiOutputNode(fragments).execute()
        output_partitions = []
        for output_partition_fragments in zip(*fragments):
            output_partition_fragments = list(output_partition_fragments)
            ray.wait(output_partition_fragments, num_returns=len(output_partition_fragments))

            output_partitions.append(
                _read_fragments.options(runtime_env=_get_runtime()).bind(*output_partition_fragments)
            )

        return RayDataset(output_partitions, new_partitioning)

    def co_group(
        self,
        others: typing.Union[typing.List["RayDataset"], "RayDataset"],
        fun: typing.Callable[[pyarrow.Table, pyarrow.Table], pyarrow.Table],
    ) -> "RayDataset":
        if isinstance(others, RayDataset):
            others = [others]

        assert all(
            self.partitioning.is_equivalent(other.partitioning) for other in others
        ), f"Partitioning must match for all datasets. Actual: {[self.partitioning, *[o.partitioning for o in others]]}"
        output_partitions = []

        for co_partitions in zip(*[self.partitions, *[other.partitions for other in others]]):
            output_partitions.append(ray.remote(fun).options(runtime_env=_get_runtime()).bind(*co_partitions))

        return RayDataset(output_partitions, self.partitioning)

    def execute(self) -> pyarrow.RecordBatchReader:
        tasks = MultiOutputNode(self.partitions).execute()
        first_table = _first_non_empty_result(tasks)

        if first_table is None:
            msg = "Execution returned empty result"
            raise RuntimeError(msg)

        schema = first_table.schema

        def wait_tasks(in_progress):
            while in_progress:
                ready_tasks, in_progress = ray.wait(in_progress, num_returns=1)
                try:
                    table = ray.get(ready_tasks[0])
                except ray.exceptions.RayTaskError as exc:
                    if isinstance(exc.cause, EmptyPartition):
                        continue
                    raise exc.cause

                yield from table.to_batches()

        return pyarrow.RecordBatchReader.from_batches(schema, wait_tasks(tasks))


def _first_non_empty_result(tasks: typing.List[ray.ObjectRef]) -> pyarrow.Table:
    while tasks:
        ready_tasks, tasks = ray.wait(tasks, num_returns=1)
        try:
            return ray.get(ready_tasks[0])
        except ray.exceptions.RayTaskError as exc:
            if isinstance(exc.cause, EmptyPartition):
                continue

            raise exc.cause
