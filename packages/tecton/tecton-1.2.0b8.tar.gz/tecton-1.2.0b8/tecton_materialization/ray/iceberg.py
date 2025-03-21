import dataclasses
import os
import uuid
from datetime import timezone
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pyarrow
from duckdb.typing import INTEGER
from pyarrow._dataset import WrittenFile
from pyarrow.filesystem import FileSystem
from pyiceberg.exceptions import CommitFailedException
from pyiceberg.expressions import And
from pyiceberg.expressions import BooleanExpression
from pyiceberg.expressions import GreaterThanOrEqual
from pyiceberg.expressions import In
from pyiceberg.expressions import LessThan
from pyiceberg.expressions.literals import TimestampLiteral
from pyiceberg.manifest import DataFile
from pyiceberg.partitioning import PartitionField
from pyiceberg.partitioning import PartitionSpec
from pyiceberg.table import TableProperties
from pyiceberg.table import _parquet_files_to_data_files
from pyiceberg.transforms import IdentityTransform
from pyiceberg.typedef import EMPTY_DICT
from pyiceberg.utils.datetime import timestamptz_to_micros

from tecton_core import conf
from tecton_core.arrow import PARQUET_WRITE_OPTIONS
from tecton_core.compute_mode import ComputeMode
from tecton_core.data_types import TimestampType
from tecton_core.iceberg_catalog import MetadataCatalog
from tecton_core.iceberg_catalog import bucket_transform
from tecton_core.offline_store import EntityBucketPartitionParams
from tecton_core.offline_store import patch_timestamps_in_arrow_schema
from tecton_core.query.dialect import Dialect
from tecton_core.query.nodes import AddAnchorTimeNode
from tecton_core.query.nodes import ConvertTimestampToUTCNode
from tecton_core.query.nodes import StagedTableScanNode
from tecton_core.query_consts import anchor_time
from tecton_core.schema import Schema
from tecton_core.schema_validation import tecton_schema_to_arrow_schema
from tecton_core.time_utils import convert_timestamp_for_version
from tecton_materialization.common.task_params import TimeInterval
from tecton_materialization.ray.offline_store_writer import OfflineStoreParams
from tecton_materialization.ray.offline_store_writer import OfflineStoreWriter
from tecton_materialization.ray.offline_store_writer import path_from_uri
from tecton_proto.common import data_type__client_pb2 as data_type_pb2
from tecton_proto.common import schema__client_pb2 as schema_pb2
from tecton_proto.offlinestore.delta.metadata__client_pb2 import TectonDeltaMetadata


PHYSICAL_PARTITION_NAME = "bucket"


@dataclasses.dataclass
class IcebergWriter(OfflineStoreWriter):
    def __init__(
        self,
        store_params: OfflineStoreParams,
        table_uri: str,
        join_keys: List[str],
        filesystem: Optional[FileSystem] = None,
    ):
        super().__init__(store_params, table_uri, join_keys)
        self._add_uris: List[str] = []
        self._deletes: List[DataFile] = []
        if filesystem:
            self._filesystem = filesystem
            self._base_path = self._table_uri
        else:
            self._filesystem, self._base_path = pyarrow.fs.FileSystem.from_uri(self._table_uri)
        self._catalog = MetadataCatalog(name="object_store_catalog", properties={})

        assert store_params.num_entity_buckets, "Iceberg offline store must be configured with `num_entity_buckets`"
        bucket_transformer_name = f"bucket_transform_{store_params.num_entity_buckets}_{uuid.uuid4().hex[:8]}"
        self._duckdb_conn.create_function(
            bucket_transformer_name, bucket_transform(store_params.num_entity_buckets), return_type=INTEGER
        )
        self._bucket_expression = f"{bucket_transformer_name}({self.join_keys_expression(self._join_keys)})"
        self._retry_exceptions = [CommitFailedException]

    def _time_limits(self, time_interval: TimeInterval) -> pyarrow.Table:
        """Returns a Table specifying the limits of data affected by a materialization job.

        :param time_interval: The feature time interval
        :returns: A relation with one column for the timestamp key and anchor time corresponding to the first column.
        The first row will be the values for feature start time and the second for feature end time.
        """
        timestamp_key = self._feature_params.time_spec.timestamp_key
        timestamp_table = pyarrow.table({timestamp_key: [time_interval.start, time_interval.end]})

        if self._feature_params.batch_schedule is None:
            msg = "Batch schedule is required for batch materialization"
            raise Exception(msg)

        tree = AddAnchorTimeNode(
            dialect=Dialect.DUCKDB,
            compute_mode=ComputeMode.RIFT,
            input_node=ConvertTimestampToUTCNode(
                dialect=Dialect.DUCKDB,
                compute_mode=ComputeMode.RIFT,
                input_node=StagedTableScanNode(
                    dialect=Dialect.DUCKDB,
                    compute_mode=ComputeMode.RIFT,
                    staged_schema=Schema.from_dict({timestamp_key: TimestampType()}),
                    staging_table_name="timestamp_table",
                ).as_ref(),
                timestamp_key=timestamp_key,
            ).as_ref(),
            feature_store_format_version=self._feature_params.feature_store_format_version,
            batch_schedule=self._feature_params.batch_schedule,
            timestamp_field=timestamp_key,
        ).as_ref()
        return self._duckdb_conn.sql(tree.to_sql()).arrow()

    def delete_time_range(self, interval: TimeInterval) -> None:
        """Filters and deletes previously materialized data within the interval.

        :param interval: The feature data time interval to delete
        """
        print(f"Clearing prior data in range {interval.start} - {interval.end}")

        time_spec = self._feature_params.time_spec

        def table_filter(input_table_to_filter: pyarrow.dataset.Dataset) -> pyarrow.Table:
            time_limit_table = self._time_limits(interval)
            # Add timezone to timestamps
            input_table_to_filter = input_table_to_filter.cast(
                patch_timestamps_in_arrow_schema(input_table_to_filter.schema)
            )
            return self._duckdb_conn.sql(
                f"""
                WITH flattened_limits AS(
                    SELECT MIN("{time_spec.time_column}") AS start, MAX("{time_spec.time_column}") AS end
                    FROM time_limit_table
                )
                SELECT input_table_to_filter.* FROM input_table_to_filter
                LEFT JOIN flattened_limits
                ON input_table_to_filter."{time_spec.time_column}" >= flattened_limits.start
                AND input_table_to_filter."{time_spec.time_column}" < flattened_limits.end
                WHERE flattened_limits.start IS NULL
            """
            ).arrow()

        if time_spec.time_column == anchor_time():
            start_time = convert_timestamp_for_version(
                interval.start, self._feature_params.feature_store_format_version
            )
            end_time = convert_timestamp_for_version(interval.end, self._feature_params.feature_store_format_version)
            predicate = And(
                GreaterThanOrEqual(time_spec.time_column, start_time), LessThan(time_spec.time_column, end_time)
            )
        else:
            start_time_str = interval.start.astimezone(timezone.utc).isoformat()
            end_time_str = interval.end.astimezone(timezone.utc).isoformat()
            start_time_lit = TimestampLiteral(timestamptz_to_micros(start_time_str))
            end_time_lit = TimestampLiteral(timestamptz_to_micros(end_time_str))
            predicate = And(
                GreaterThanOrEqual(time_spec.time_column, start_time_lit), LessThan(time_spec.time_column, end_time_lit)
            )
        self._filter_files_for_deletion(predicate, table_filter)

    def _filter_files_for_deletion(
        self,
        predicate: BooleanExpression,
        filter_table: Callable[[pyarrow.dataset.Dataset], pyarrow.Table],
        force_overwrite: bool = False,
        **write_kwargs,
    ):
        if not self._catalog.table_exists(self._table_uri):
            return

        tbl = self._catalog.load_table(self._table_uri)
        plan_files = tbl.scan(
            row_filter=predicate,
        ).plan_files()
        deletes = []
        for plan_file in plan_files:
            input_table = pyarrow.dataset.dataset(
                source=path_from_uri(plan_file.file.file_path),
                filesystem=self._filesystem,
            ).to_table()
            output_table = filter_table(input_table)
            if input_table.num_rows != output_table.num_rows or force_overwrite:
                deletes.append(plan_file.file)
                if output_table.num_rows:
                    self.write(output_table, bucket_and_sort=False, **write_kwargs)
        self._deletes.extend(deletes)

    def write(
        self,
        input_table: Union[pyarrow.Table, pyarrow.RecordBatchReader],
        tags: Optional[Dict[str, str]] = None,
        bucket_and_sort: bool = True,
    ) -> List[str]:
        """Writes a pyarrow Table to the base_uri.

        Args:
            input_table: The input pyarrow Table or RecordBatchReader.
            tags: Optional metadata tags.
            bucket_and_sort: If True, compute bucketing and sorting using DuckDB.
                             If False, assume bucketing is already done and just add the physical partition column.

        Returns:
            List[str]: URIs for the written files.

        This does NOT commit. Call commit() after calling this to commit your changes.
        """
        if bucket_and_sort:
            # Perform bucketing and sorting in DuckDB
            self._duckdb_conn.register("input_table", input_table)
            query = f"""
                SELECT
                    *,
                    {self._bucket_expression} AS {EntityBucketPartitionParams.partition_by},
                    {EntityBucketPartitionParams.partition_by} AS {PHYSICAL_PARTITION_NAME}
                FROM input_table
                ORDER BY {self._feature_params.time_spec.time_column};
            """
            bucketed_table = self._duckdb_conn.sql(query).arrow()
        else:
            # add the physical partition column if needed
            if PHYSICAL_PARTITION_NAME not in input_table.schema.names:
                input_table = input_table.append_column(
                    PHYSICAL_PARTITION_NAME, input_table.column(EntityBucketPartitionParams.partition_by)
                )
            bucketed_table = input_table

        adds = []
        failed = False

        def visit_file(f: WrittenFile):
            try:
                path = f.path
                _, prefix, relative = path.partition(self._base_path)
                assert prefix == self._base_path, f"Written path is not relative to base path: {path}"
                uri = self._table_uri + relative
                adds.append(uri)
            except Exception as e:
                # Pyarrow logs and swallows exceptions from this function, so we need some other way of knowing there
                # was a failure
                nonlocal failed
                failed = True
                raise e

        # TODO: consider using duckdb to write the parquet files directly
        max_rows_per_file = conf.get_or_none("PARQUET_MAX_ROWS_PER_FILE")
        max_rows_per_group = conf.get_or_none("PARQUET_MAX_ROWS_PER_GROUP")
        pyarrow.dataset.write_dataset(
            data=bucketed_table,
            filesystem=self._filesystem,
            base_dir=self._base_path,
            format=pyarrow.dataset.ParquetFileFormat(),
            file_options=PARQUET_WRITE_OPTIONS,
            basename_template=f"{uuid.uuid4()}-part-{{i}}.parquet",
            partitioning=pyarrow.dataset.partitioning(
                pyarrow.schema([(PHYSICAL_PARTITION_NAME, pyarrow.int32())]),
                flavor="hive",
            ),
            file_visitor=visit_file,
            existing_data_behavior="overwrite_or_ignore",
            max_partitions=365 * 100,
            max_rows_per_file=int(max_rows_per_file) if max_rows_per_file else 0,
            max_rows_per_group=int(max_rows_per_group) if max_rows_per_group else 1_000_000,
            use_threads=True,
        )

        if failed:
            msg = "file visitor failed during write"
            raise Exception(msg)

        self._add_uris.extend(adds)
        return adds

    def delete_keys(self, keys: pyarrow.Table):
        """Deletes keys from the offline store."""

        def filter_table(input_table_filter_keys: pyarrow.dataset.Dataset) -> pyarrow.Table:
            """Filters for the other keys that are not in the set of keys to delete"""
            return self._duckdb_conn.sql(
                f"""
                SELECT * FROM input_table_filter_keys
                ANTI JOIN keys
                USING ({", ".join(keys.column_names)})
                """
            ).arrow()

        result = self._duckdb_conn.sql(f"""
            SELECT
                DISTINCT {self._bucket_expression} AS {EntityBucketPartitionParams.partition_by}
            FROM keys
        """).fetchall()
        entity_buckets = [row[0] for row in result]
        predicate = In(EntityBucketPartitionParams.partition_by, entity_buckets)
        return self._filter_files_for_deletion(predicate, filter_table)

    def commit(self, metadata: Optional[TectonDeltaMetadata] = None) -> Optional[int]:
        """commits files to the offline store."""
        if not self._add_uris and not self._deletes:
            # nothing to commit
            return
        try:
            if len(self._add_uris) != len(set(self._add_uris)):
                msg = "`_add_uris` file paths must be unique"
                raise ValueError(msg)

            if len(self._deletes) != len(set(self._deletes)):
                msg = "`_deletes` file paths must be unique"
                raise ValueError(msg)

            # pyiceberg 0.8.1 does not support 'ns' timestamp precision so we need this option.
            os.environ["PYICEBERG_DOWNCAST_NS_TIMESTAMP_TO_US_ON_WRITE"] = "true"
            if not self._catalog.table_exists(self._table_uri):
                feature_schema_proto = self._feature_params.schema

                # ensure that "_anchor_time" exists in the schema even for temporal fv
                if not any(col.name == anchor_time() for col in feature_schema_proto.columns):
                    anchor_time_column = schema_pb2.Column(
                        name=anchor_time(),
                        offline_data_type=data_type_pb2.DataType(type=data_type_pb2.DataTypeEnum.DATA_TYPE_INT64),
                    )
                    feature_schema_proto.columns.append(anchor_time_column)

                if not any(
                    col.name == EntityBucketPartitionParams.partition_by for col in feature_schema_proto.columns
                ):
                    partition_column = schema_pb2.Column(
                        name=EntityBucketPartitionParams.partition_by,
                        offline_data_type=data_type_pb2.DataType(type=data_type_pb2.DataTypeEnum.DATA_TYPE_INT32),
                    )
                    feature_schema_proto.columns.append(partition_column)

                tecton_schema = Schema(feature_schema_proto)
                pa_schema = tecton_schema_to_arrow_schema(tecton_schema)
                # TODO: have the bucket transformer also defined in the spec.
                #  requires us to rewrite pyiceberg `parquet_files_to_data_files` since it's a non-linear transformation.
                partition_spec = PartitionSpec(
                    PartitionField(
                        source_id=-1,
                        field_id=-1,
                        transform=IdentityTransform(),
                        name=EntityBucketPartitionParams.partition_by,
                    )
                )
                tbl = self._catalog.create_table(
                    self._table_uri, pa_schema, self._table_uri, partition_spec=partition_spec
                )
            else:
                tbl = self._catalog.load_table(self._table_uri)

            with tbl.transaction() as tx:
                snapshot_properties = (
                    {"featureStartTime": metadata.feature_start_time.seconds} if metadata else EMPTY_DICT
                )
                if tx.table_metadata.name_mapping() is None:
                    tx.set_properties(
                        **{
                            TableProperties.DEFAULT_NAME_MAPPING: tx.table_metadata.schema().name_mapping.model_dump_json()
                        }
                    )
                with tx.update_snapshot(snapshot_properties=snapshot_properties).overwrite() as update_snapshot:
                    add_data_files = _parquet_files_to_data_files(
                        table_metadata=tbl.metadata, file_paths=self._add_uris, io=tbl.io
                    )
                    for add_data_file in add_data_files:
                        update_snapshot.append_data_file(add_data_file)
                    for delete_data_file in self._deletes:
                        update_snapshot.delete_data_file(delete_data_file)
        except tuple(self._retry_exceptions):
            # Commit should be retried together with new write.
            self.abort()
            raise
        finally:
            self._reset_state()

    def transaction_exists(self, metadata: TectonDeltaMetadata) -> bool:
        """checks matching transaction metadata, which signals that a previous task attempt already wrote data
        If the task overwrites a previous materialization task interval then we treat it as a new transaction.

        :param metadata: transaction metadata
        :return: whether the same transaction has been executed before
        """
        if not self._catalog.table_exists(self._table_uri):
            return False

        tbl = self._catalog.load_table(self._table_uri)
        for snapshot in tbl.metadata.snapshots:
            if snapshot.summary["featureStartTime"] == metadata.feature_start_time.seconds:
                return True
        return False

    def abort(self):
        """
        Abort the transaction by cleaning up any files and state.
        Clean up created parquet files that were not part of a successful commit.
        """
        for add_file in self._add_uris:
            self._filesystem.delete_file(path_from_uri(add_file))
        self._reset_state()

    def _reset_state(self):
        self._add_uris = []
        self._deletes = []

    @staticmethod
    def join_keys_expression(join_keys: List[str]):
        # TODO: make the partition scheme more explicit so that the customer can define which key(s) to bucket.
        return join_keys[0]
