import logging
import os
from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple

import attrs
import pandas
import pyarrow
import pyarrow.dataset

from tecton_core import conf
from tecton_core import duckdb_factory
from tecton_core import specs
from tecton_core.compute_mode import ComputeMode
from tecton_core.duckdb_factory import DuckDBConfig
from tecton_core.embeddings.model_artifacts import DEFAULT_MODEL_PROVIDER
from tecton_core.embeddings.model_artifacts import ModelArtifactProvider
from tecton_core.errors import TectonInternalError
from tecton_core.offline_store import DEFAULT_OPTIONS_PROVIDERS
from tecton_core.offline_store import OfflineStoreOptionsProvider
from tecton_core.offline_store import get_s3_options_for_fd
from tecton_core.query.data_sources import FileDataSourceScanNode
from tecton_core.query.data_sources import PushTableSourceScanNode
from tecton_core.query.data_sources import RedshiftDataSourceScanNode
from tecton_core.query.dialect import Dialect
from tecton_core.query.duckdb.compute import DuckDBCompute
from tecton_core.query.duckdb.nodes import IcebergOfflineStoreScanNode
from tecton_core.query.duckdb.rewrite import DuckDBTreeRewriter
from tecton_core.query.errors import UserDefinedTransformationError
from tecton_core.query.executor_params import ExecutionContext
from tecton_core.query.executor_params import QueryTreeStep
from tecton_core.query.executor_utils import DebugOutput
from tecton_core.query.executor_utils import QueryTreeMonitor
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.node_interface import Partitioning
from tecton_core.query.node_interface import PartitionSelector
from tecton_core.query.node_interface import SinglePartition
from tecton_core.query.node_utils import get_first_input_node_of_class
from tecton_core.query.node_utils import get_pipeline_dialect
from tecton_core.query.node_utils import get_staging_nodes
from tecton_core.query.nodes import AddPartitionColumn
from tecton_core.query.nodes import AsofJoinFullAggNode
from tecton_core.query.nodes import AsofJoinNode
from tecton_core.query.nodes import DataSourceScanNode
from tecton_core.query.nodes import EntityFilterNode
from tecton_core.query.nodes import FeatureViewPipelineNode
from tecton_core.query.nodes import JoinNode
from tecton_core.query.nodes import MultiOdfvPipelineNode
from tecton_core.query.nodes import OfflineStoreScanNode
from tecton_core.query.nodes import RenameColsNode
from tecton_core.query.nodes import Repartition
from tecton_core.query.nodes import StagedTableScanNode
from tecton_core.query.nodes import StagingNode
from tecton_core.query.nodes import TextEmbeddingInferenceNode
from tecton_core.query.nodes import UserSpecifiedDataNode
from tecton_core.query.optimize.adaptive import should_use_optimized_full_aggregate_node
from tecton_core.query.pandas.node import ArrowExecNode
from tecton_core.query.pandas.nodes import PandasDataSourceScanNode
from tecton_core.query.pandas.nodes import PandasFeatureViewPipelineNode
from tecton_core.query.pandas.nodes import PandasMultiOdfvPipelineNode
from tecton_core.query.pandas.nodes import PandasRenameColsNode
from tecton_core.query.pandas.nodes import PyArrowDataSourceScanNode
from tecton_core.query.query_tree_compute import ArrowCompute
from tecton_core.query.query_tree_compute import QueryTreeCompute
from tecton_core.query.query_tree_compute import SQLCompute
from tecton_core.query.ray.dataset import RayDataset
from tecton_core.secret_management import SecretResolver
from tecton_core.snowflake_context import SnowflakeContext


logger = logging.getLogger(__name__)


def _pyarrow_type_contains_map_type(pyarrow_type: pyarrow.DataType) -> bool:
    if isinstance(pyarrow_type, pyarrow.MapType):
        return True
    elif isinstance(pyarrow_type, pyarrow.StructType):
        return any(_pyarrow_type_contains_map_type(field.type) for field in pyarrow_type)
    elif isinstance(pyarrow_type, pyarrow.ListType):
        return _pyarrow_type_contains_map_type(pyarrow_type.value_type)
    return False


@dataclass
class QueryTreeOutput:
    output: pyarrow.RecordBatchReader

    @property
    def result_df(self) -> pandas.DataFrame:
        contains_map_type = any(_pyarrow_type_contains_map_type(field.type) for field in self.output.schema)
        if contains_map_type:
            # The `maps_as_pydicts` parameter for pyarrow.Table.to_pandas is only supported starting in pyarrow 13.0.0.
            if pyarrow.__version__ < "13.0.0":
                msg = f"Rift requires pyarrow>=13.0.0 to perform feature retrieval for Map features. You have version {pyarrow.__version__}."
                raise RuntimeError(msg)
            return self.output.read_pandas(maps_as_pydicts="strict")

        return self.output.read_pandas()

    @property
    def result_table(self) -> "pyarrow.RecordBatchReader":
        return self.output


UserErrors = (UserDefinedTransformationError,)


def get_data_source_dialect_and_physical_node(
    node: DataSourceScanNode,
) -> Tuple[Dialect, Optional[ArrowExecNode]]:
    batch_source = node.ds.batch_source
    if isinstance(batch_source, specs.PandasBatchSourceSpec):
        exec_node = PandasDataSourceScanNode.from_node_inputs(query_node=node, input_node=None)
        return Dialect.ARROW, exec_node
    elif isinstance(batch_source, specs.PyArrowBatchSourceSpec):
        exec_node = PyArrowDataSourceScanNode.from_node_inputs(query_node=node, input_node=None)
        return Dialect.ARROW, exec_node
    elif isinstance(batch_source, specs.FileSourceSpec):
        exec_node = FileDataSourceScanNode.from_node_input(node)
        return Dialect.ARROW, exec_node
    elif isinstance(
        batch_source,
        specs.PushTableSourceSpec,
    ):
        exec_node = PushTableSourceScanNode.from_node_input(node)
        return Dialect.ARROW, exec_node
    elif isinstance(batch_source, specs.SnowflakeSourceSpec):
        return Dialect.SNOWFLAKE, None
    elif isinstance(batch_source, specs.BigquerySourceSpec):
        return Dialect.BIGQUERY, None
    elif isinstance(batch_source, specs.RedshiftSourceSpec):
        return Dialect.ARROW, RedshiftDataSourceScanNode.from_node_input(node)

    msg = f"Unexpected data source type encountered: {batch_source.__class__}"
    raise Exception(msg)


def rewrite_data_sources(plan: NodeRef) -> None:
    """
    Inferring dialect for data source nodes and propagating it to the closest StagingNode.
    There are two kinds of data sources: sql-based and arrow-based.
    For arrow-based sources DataSourceScanNode is replaced with concrete implementation based on source type.
    """
    staging_nodes = get_staging_nodes(plan, QueryTreeStep.DATA_SOURCE, as_ref=True)
    if not staging_nodes:
        return

    for _, staging_node in staging_nodes.items():
        scan_node = get_first_input_node_of_class(staging_node, DataSourceScanNode)
        if not scan_node:
            continue

        dialect, physical_node = get_data_source_dialect_and_physical_node(scan_node)
        if physical_node:
            # replacing DataSourceScanNode
            staging_node.node = attrs.evolve(staging_node.node, dialect=dialect, input_node=physical_node.as_ref())
        else:
            # data source has SQL-based dialect
            # just need to propagate correct dialect to the StagingNode
            staging_node.node = attrs.evolve(staging_node.node, dialect=dialect)


def rewrite_offline_scan_node(
    plan: NodeRef, offline_store_options_providers: Iterable[OfflineStoreOptionsProvider]
) -> None:
    staging_nodes = get_staging_nodes(plan, QueryTreeStep.OFFLINE_STORE, as_ref=True)
    if not staging_nodes:
        return

    for _, staging_node in staging_nodes.items():
        offline_scan_node = get_first_input_node_of_class(staging_node, OfflineStoreScanNode)
        if not offline_scan_node:
            continue

        if offline_scan_node.feature_definition_wrapper.has_iceberg_offline_store:
            physical_node = IcebergOfflineStoreScanNode.from_query_node(
                query_node=offline_scan_node,
                offline_store_options_providers=offline_store_options_providers,
            )
            staging_node.node = attrs.evolve(
                staging_node.node, input_node=physical_node.as_ref(), dialect=Dialect.ARROW
            )


def _rewrite_pandas_pipeline(plan: NodeRef) -> None:
    def traverse(tree: NodeRef) -> None:
        if isinstance(tree.node, FeatureViewPipelineNode):
            pipeline_node = tree.node
            # We don't need to rewrite inputs, because we assume that all inputs are StagingNodes
            assert all(
                isinstance(input_ref.node, StagingNode) for input_ref in pipeline_node.inputs_map.values()
            ), "All inputs to FeatureViewPipelineNode are expected to be StagingNode"

            physical_node = PandasFeatureViewPipelineNode.from_node_inputs(
                query_node=pipeline_node,
                input_node=None,
            )

            tree.node = StagingNode(
                dialect=Dialect.ARROW,
                compute_mode=ComputeMode.RIFT,
                input_node=physical_node.as_ref(),
                staging_table_name=f"pandas_pipeline_{pipeline_node.feature_definition_wrapper.name}",
            )
            return

        for i in tree.inputs:
            traverse(tree=i)

    traverse(plan)


def rewrite_pipeline_nodes(plan: NodeRef) -> None:
    """
    When pipeline mode is "pandas"/"python" the logical node is replaced with PandasFeatureViewPipelineNode + StagingNode.
    The latter is needed to indicate that this should be executed by ArrowCompute.

    In other cases (sql-based transformations): propagate correct dialect to the closest staging node.
    For now, all pipeline nodes are expected to have the same dialect.
    """
    pipeline_dialect = get_pipeline_dialect(plan)
    if pipeline_dialect == Dialect.PANDAS:
        _rewrite_pandas_pipeline(plan)
        return

    if not pipeline_dialect:
        return

    staging_nodes = get_staging_nodes(plan, QueryTreeStep.PIPELINE, as_ref=True)
    for _, staging_node in staging_nodes.items():
        staging_node.node = attrs.evolve(staging_node.node, dialect=pipeline_dialect)


def rewrite_rtfvs(plan: NodeRef) -> None:
    """
    Logical node MultiOdfvPipelineNode is replaced with PandasMultiOdfvPipelineNode,
    which handles both "pandas" and "python" modes.

    If MultiOdfvPipelineNode is succeeded by RenameColsNode it should as well replaced by PandasRenameColsNode
    to minimize switching between Arrow and DuckDB computes.
    """

    def create_physical_odfv_pipeline_node(logical_node: MultiOdfvPipelineNode) -> ArrowExecNode:
        return PandasMultiOdfvPipelineNode.from_node_inputs(logical_node, logical_node.input_node)

    def create_physical_rename_node(logical_node: RenameColsNode, odfv_pipeline_node: NodeRef) -> ArrowExecNode:
        return PandasRenameColsNode.from_node_inputs(logical_node, odfv_pipeline_node)

    def traverse(tree: NodeRef) -> None:
        if isinstance(tree.node, RenameColsNode) and isinstance(tree.node.input_node.node, MultiOdfvPipelineNode):
            tree.node = StagingNode(
                dialect=Dialect.ARROW,
                compute_mode=ComputeMode.RIFT,
                input_node=create_physical_rename_node(
                    tree.node, create_physical_odfv_pipeline_node(tree.node.input_node.node).as_ref()
                ).as_ref(),
                staging_table_name="rtfv_output",
            )
            return

        if isinstance(tree.node, MultiOdfvPipelineNode):
            tree.node = StagingNode(
                dialect=Dialect.ARROW,
                compute_mode=ComputeMode.RIFT,
                input_node=create_physical_odfv_pipeline_node(tree.node).as_ref(),
                staging_table_name="rtfv_output",
            )
            return

        for i in tree.inputs:
            traverse(tree=i)

    traverse(plan)


def rewrite_user_input(plan: NodeRef) -> None:
    """
    UserSpecifiedDataNode is wrapped into StagingNode with Arrow dialect
    to force executor use ArrowCompute and call .to_arrow_reader() instead of .to_sql()
    """

    def traverse(tree: NodeRef) -> None:
        if isinstance(tree.node, UserSpecifiedDataNode):
            tree.node = StagingNode(
                dialect=Dialect.ARROW,
                compute_mode=ComputeMode.RIFT,
                input_node=tree.node.as_ref(),
                staging_table_name=tree.node.data._temp_table_name,
            )
            return

        for i in tree.inputs:
            traverse(tree=i)

    traverse(plan)


def rewrite_embedding_nodes(plan: NodeRef) -> None:
    """
    UserSpecifiedDataNode is wrapped into StagingNode with Arrow dialect
    to force executor use ArrowCompute and call .to_arrow_reader() instead of .to_sql()
    """

    def traverse(tree: NodeRef) -> None:
        if isinstance(tree.node, TextEmbeddingInferenceNode):
            from tecton_core.embeddings.nodes import ArrowExecTextEmbeddingInferenceNode

            tree.node = ArrowExecTextEmbeddingInferenceNode.from_node_input(tree.node)
            return

        for i in tree.inputs:
            traverse(tree=i)

    traverse(plan)


def check_partitioning_compatibility(plan: NodeRef) -> None:
    def get_all_join_nodes(node_ref: NodeRef) -> Iterable[NodeRef]:
        if isinstance(node_ref.node, (JoinNode, AsofJoinNode, AsofJoinFullAggNode, EntityFilterNode)):
            yield node_ref

        for child in node_ref.inputs:
            yield from get_all_join_nodes(child)

    def determine_side_to_repartition(
        left: NodeRef, right: NodeRef
    ) -> Tuple[Optional[NodeRef], Optional[Partitioning]]:
        left_partitioning = left.output_partitioning
        right_partitioning = right.output_partitioning

        if left_partitioning and right_partitioning and left_partitioning.is_equivalent(right_partitioning):
            return None, None

        left_not_partitioned = left_partitioning in (None, SinglePartition())
        right_not_partitioned = right_partitioning in (None, SinglePartition())

        # if both side are partitioned
        if not left_not_partitioned and not right_not_partitioned:
            # select the side with fewer partitions to repartition
            # (assuming fewer partitions means less data)
            if left_partitioning.number_of_partitions > right_partitioning.number_of_partitions:
                return right, left_partitioning
            else:
                return left, right_partitioning

        if left_not_partitioned:
            return left, right_partitioning

        return right, left_partitioning

    for join_node in get_all_join_nodes(plan):
        left_input, right_input = join_node.inputs

        repartition_side, partitioning = determine_side_to_repartition(left_input, right_input)
        if not repartition_side:
            continue

        repartition_attr = Repartition(partitioning=partitioning, key="partition_key")

        if isinstance(repartition_side.node, StagingNode) and repartition_side.node.dialect == Dialect.DUCKDB:
            repartition_side.node = attrs.evolve(
                repartition_side.node,
                repartition=repartition_attr,
            )
        else:
            repartition_side.node = StagingNode(
                dialect=Dialect.DUCKDB,
                compute_mode=ComputeMode.RIFT,
                input_node=repartition_side.node.as_ref(),
                repartition=repartition_attr,
                staging_table_name="repartition",
            )

        staging_input = repartition_side.node.input_node
        staging_input.node = AddPartitionColumn(
            dialect=staging_input.node.dialect,
            compute_mode=staging_input.node.compute_mode,
            input_node=staging_input.node.as_ref(),
            partition_column="partition_key",
            partition_expr=partitioning.partition_expression,
        )


def logical_plan_to_physical_plan(
    logical_plan: NodeRef,
    use_optimized_full_agg: bool = False,
    offline_store_options_providers: Optional[Iterable[OfflineStoreOptionsProvider]] = None,
) -> NodeRef:
    physical_plan = logical_plan.deepcopy()

    # replace some generic nodes with Rift specific
    # ToDo: this can be removed when Athena and Snowflake are removed
    # and the code can be moved to generic nodes
    rewriter = DuckDBTreeRewriter()
    rewriter.rewrite(physical_plan, use_optimized_full_agg)

    rewrite_data_sources(physical_plan)
    rewrite_offline_scan_node(physical_plan, offline_store_options_providers)
    rewrite_pipeline_nodes(physical_plan)
    rewrite_rtfvs(physical_plan)
    rewrite_user_input(physical_plan)
    rewrite_embedding_nodes(physical_plan)
    check_partitioning_compatibility(physical_plan)

    return physical_plan


def _execute_stage(
    context: ExecutionContext,
    output_node_ref: NodeRef,
    input_nodes_ref: List[NodeRef],
    inputs: List[pyarrow.Table],
    partition_selector: Optional[PartitionSelector] = None,
    duckdb_home_dir: Optional[str] = None,
    snowflake_connection_params: Optional[Dict[str, Any]] = None,
) -> pyarrow.Table:
    conf.set("TECTON_OFFLINE_RETRIEVAL_COMPUTE_MODE", "rift")

    if duckdb_home_dir:
        duckdb_factory.set_home_dir_override(duckdb_home_dir)

    if snowflake_connection_params:
        SnowflakeContext.set_connection_params(snowflake_connection_params)

    compute = _get_or_create_compute_by_dialect(output_node_ref.node.dialect, context, output_node_ref)

    if isinstance(compute, ArrowCompute):
        reader = compute.run(
            output_node_ref, input_nodes_ref, input_data=inputs, context=context, partition_selector=partition_selector
        )
    elif isinstance(compute, SQLCompute):
        with compute:
            for input_node_ref, input_table in zip(input_nodes_ref, inputs):
                assert isinstance(input_node_ref.node, StagedTableScanNode)

                table_name = input_node_ref.node.staging_table_name
                compute.register_temp_table(table_name, input_table)

            node = output_node_ref.node
            sql_string = node.with_dialect(compute.get_dialect())._to_staging_query_sql(partition_selector)
            expected_output_schema = node.output_schema if len(node.output_schema) else None

            if isinstance(compute, DuckDBCompute):
                if isinstance(node, OfflineStoreScanNode):
                    s3_options = get_s3_options_for_fd(
                        node.feature_definition_wrapper, context.offline_store_options_providers
                    )
                else:
                    s3_options = None
                reader = compute.run_sql(
                    sql_string,
                    return_dataframe=True,
                    expected_output_schema=expected_output_schema,
                    monitor=None,
                    checkpoint_as=None,
                    s3_options=s3_options,
                )
            else:
                reader = compute.run_sql(
                    sql_string,
                    return_dataframe=True,
                    expected_output_schema=expected_output_schema,
                    monitor=None,
                    checkpoint_as=None,
                )
    else:
        msg = f"Unrecognized type of compute: {type(compute)}"
        raise TectonInternalError(msg)

    return reader.read_all()


def convert_plan_to_ray_dag(node_ref: NodeRef, context: ExecutionContext, **kwargs: Any) -> RayDataset:
    assert isinstance(node_ref.node, StagingNode)

    def find_inputs(input_: NodeRef, output: StagingNode) -> Iterable[NodeRef]:
        if (
            isinstance(input_.node, StagingNode)
            and input_.node != output
            and (input_.node.dialect != output.dialect or input_.node.checkpoint or input_.node.repartition)
        ):
            # Only staging nodes of different dialect count as input to the current stage
            # or we encountered a staging node with "checkpoint" enabled
            yield input_
            return

        for input_ in input_.inputs:
            yield from find_inputs(input_, output)

    inputs = list(find_inputs(node_ref, node_ref.node))

    child_ray_datasets = [
        convert_plan_to_ray_dag(
            input_node.node.as_ref(),  # create a copy
            context,
            **kwargs,
        )
        for input_node in inputs
    ]

    for input_node_ref in inputs:
        input_node_ref.node = StagedTableScanNode.from_staging_node(
            dialect=input_node_ref.node.dialect, compute_mode=ComputeMode.RIFT, query_node=input_node_ref.node
        )

    if not child_ray_datasets:

        def _partition_generator(partition_selector: PartitionSelector) -> pyarrow.Table:
            return _execute_stage(context, node_ref, inputs, partition_selector=partition_selector, inputs=[], **kwargs)

        # This still needs a partition selection
        dataset = RayDataset.from_partition_generator(_partition_generator, node_ref.output_partitioning)

    elif len(child_ray_datasets) == 1:
        input_ray_dataset = child_ray_datasets.pop()

        def _map_fn(input_table: pyarrow.Table) -> pyarrow.Table:
            return _execute_stage(context, node_ref, inputs, inputs=[input_table], **kwargs)

        dataset = input_ray_dataset.map(_map_fn)
    else:

        def _co_group_fn(*input_tables: Tuple[pyarrow.Table]) -> pyarrow.Table:
            assert len(inputs) == len(
                input_tables
            ), f"Number of actual inputs doesn't match expected {len(inputs)} != {len(input_tables)}"

            return _execute_stage(context, node_ref, inputs, inputs=list(input_tables), **kwargs)

        left = child_ray_datasets[0]
        others = child_ray_datasets[1:]

        dataset = left.co_group(others, _co_group_fn)

    repartition = node_ref.node.repartition
    if repartition:
        dataset = dataset.repartition_by(repartition.partitioning, repartition.key)

    return dataset


@attrs.define
class QueryTreeExecutor:
    offline_store_options_providers: Iterable[OfflineStoreOptionsProvider] = DEFAULT_OPTIONS_PROVIDERS
    secret_resolver: Optional[SecretResolver] = None
    model_artifact_provider: Optional[ModelArtifactProvider] = DEFAULT_MODEL_PROVIDER
    monitor: QueryTreeMonitor = DebugOutput()
    is_debug: bool = attrs.field(init=False)
    # TODO: Put duckdb_config in a map when we have more configs for different dialects.
    duckdb_config: Optional[DuckDBConfig] = None
    _dialect_to_compute_map: Dict[Dialect, QueryTreeCompute] = {}
    # Used to track temp tables per dialect so we can clean them up appropriately & avoid re-registering duplicates
    _dialect_to_temp_table_name: Optional[Dict[Dialect, set]] = attrs.field(init=False)

    def __attrs_post_init__(self):
        self.is_debug = conf.get_bool("DUCKDB_DEBUG")
        self._dialect_to_temp_table_name = None

    def exec_qt(self, logical_plan: NodeRef) -> QueryTreeOutput:
        # Make copy so the execution doesn't mutate the original QT visible to users

        physical_plan = logical_plan_to_physical_plan(
            logical_plan,
            use_optimized_full_agg=should_use_optimized_full_aggregate_node(logical_plan),
            offline_store_options_providers=self.offline_store_options_providers,
        )
        if self.is_debug:
            logger.warning("---------------------------------- Executing overall QT ----------------------------------")
            logger.warning(f"QT: \n{logical_plan.pretty_str()}")
            logger.warning("---------------------------------- Physical plan -----------------------------------------")
            logger.warning(f"QT: \n{physical_plan.pretty_str()}")

        context = ExecutionContext(
            offline_store_options_providers=self.offline_store_options_providers,
            secret_resolver=self.secret_resolver,
            model_artifact_provider=self.model_artifact_provider,
            duckdb_config=self.duckdb_config,
        )

        if not isinstance(physical_plan.node, StagingNode):
            # for simplicity plan should always have StagingNode at the root
            physical_plan = StagingNode(
                dialect=Dialect.DUCKDB,
                compute_mode=ComputeMode.RIFT,
                input_node=physical_plan,
                staging_table_name="",
            ).as_ref()

        ray_dataset = convert_plan_to_ray_dag(
            physical_plan,
            context,
            duckdb_home_dir=os.environ.get("TEST_TMPDIR"),
            snowflake_connection_params=SnowflakeContext.get_instance().get_connection_params()
            if SnowflakeContext.is_initialized()
            else None,
        )

        outputs = ray_dataset.execute()
        return QueryTreeOutput(output=outputs)


_dialect_to_compute_map = {}


def _get_or_create_compute_by_dialect(
    dialect: Dialect,
    context: ExecutionContext,
    qt_root: Optional[NodeRef] = None,
) -> QueryTreeCompute:
    if dialect in _dialect_to_compute_map:
        return _dialect_to_compute_map[dialect]

    compute = QueryTreeCompute.for_dialect(dialect, context, qt_root)
    _dialect_to_compute_map[dialect] = compute
    return compute
