from pyspark.sql import SparkSession
from typing import Any, Dict
from lakehouse.utils import assertion
from lakehouse.spark.etlutils.interface import Interface
from lakehouse.utils.lhlogging import log


class ETLTblProperties(Interface):
    """A generic class executing optimizations

    Use the function optimize() to set the optimize configs. Use _optimize() to execute the optimize process.

    Attributes:
        spark (SparkSession): Spark Session as provided to process the data
        options (Dict[str, Any]): Kwargs, Any options provided into the class
        catalog (str): Name of the created catalog recognized by spark e.g. from Hive Metastore or Unity Catalogue
        source_schema (str): Name of the source_schema
        target_schema (str): Name of the target_schema
    """

    def __init__(
        self,
        spark: SparkSession,
        catalog: str,
        source_schema: str,
        target_schema: str,
        **options: Dict[str, Any],
    ) -> None:
        """Initializes the TblProperties class with user-provided options.

        Args:
            spark (SparkSession): existing Spark Session
            catalog (str): Name of the created catalog recognized by spark e.g. from Hive Metastore or Unity Catalogue, required
            source_schema (str): Name of the source_schema, required
            target_schema (str): Name of the target_schema, required
            **options (Dict[str, Any]): Kwargs, Any other options provided into the class
        """
        Interface.__init__(
            self, spark, catalog, source_schema, target_schema, **options
        )
        self._tbl_properties = {"exec": False}

    def _tblproperties_with_opts(self, opts: Dict[str, Any] | None = None) -> None:
        """Function to assert allowed tblproperties options and set them.

        Args:
            opts (Dict[str, Any] | None): tblproperties options
        """
        if opts:
            assertion.assert_allowed_opts(
                opts,
                [
                    "clusterby",
                    "deletion_vectors",
                    "auto_compact",
                    "optimize_write",
                    "change_data_feed",
                    "parallel_delete_vacuum",
                    "row_tracking",
                    "type_widening",
                    "tblproperties",
                ],
            )
            self.tblproperties(**opts)
        else:
            self.tblproperties()

    def tblproperties(
        self,
        clusterby: list[str] | None = None,
        deletion_vectors: bool = True,
        auto_compact: bool = True,
        optimize_write: bool = True,
        change_data_feed: bool = True,
        row_tracking: bool = True,
        type_widening: bool = False,
        tblproperties: Dict[str, str] | None = None,
    ):
        """Function to set the optimize configs.

        Args:
            clusterby (list[str] | None): list of cols to be liquid clustered
            deletion_vectors (bool): enable deletion vectors (delta.enableDeletionVectors), default True, see also here: https://docs.delta.io/latest/delta-deletion-vectors.html
            auto_compact (bool): enable auto optimize (delta.autoOptimize.autoCompact), default True: https://docs.delta.io/latest/optimizations-oss.html#auto-compaction
            optimize_write (bool): enable optimize write (delta.autoOptimize.optimizeWrite), default True, see also here: https://docs.delta.io/latest/optimizations-oss.html#optimized-write
            change_data_feed (bool): enable change data feed, default True (delta.enableChangeDataFeed): https://docs.delta.io/latest/delta-change-data-feed.html
            row_tracking (bool): enable row tracking (delta.enableRowTracking), default True: https://docs.delta.io/latest/delta-row-tracking.html
            type_widening (bool): enable type widening (delta.enableTypeWidening), default False: https://docs.delta.io/latest/delta-type-widening.html
            tblproperties (Dict[str, str] | None): dict of any delta tblproperties as to https://docs.delta.io/

        Returns:
            self
        """
        options = {
            "clusterby": clusterby,
            "deletion_vectors": deletion_vectors,
            "auto_compact": auto_compact,
            "optimize_write": optimize_write,
            "change_data_feed": change_data_feed,
            "row_tracking": row_tracking,
            "type_widening": type_widening,
            "tblproperties": tblproperties,
        }
        assertion.assert_tblproperties(options)
        for options, value in options.items():
            self._tbl_properties[options] = value
        self._tbl_properties["exec"] = True
        return self

    @log("tblproperties", 1)
    def _tblproperties(self, table: str) -> None:
        """Function orchestrating the tblproperties

        executes the clusterby and seeting the tblproperties

        Args:
            table (str): name of the table
        """
        tbl_name = f"{self.catalog}.{self.target_schema}.{table}"
        self._clusterby(tbl_name, self._tbl_properties["clusterby"])
        self._set_delta_tblproperty(
            tbl_name,
            "delta.enableDeletionVectors",
            str(self._tbl_properties["deletion_vectors"]).lower(),
        )
        self._set_delta_tblproperty(
            tbl_name,
            "delta.autoOptimize.autoCompact",
            str(self._tbl_properties["auto_compact"]).lower(),
        )
        self._set_delta_tblproperty(
            tbl_name,
            "delta.autoOptimize.optimizeWrite",
            str(self._tbl_properties["optimize_write"]).lower(),
        )
        self._set_delta_tblproperty(
            tbl_name,
            "delta.enableChangeDataFeed",
            str(self._tbl_properties["change_data_feed"]).lower(),
        )
        self._set_delta_tblproperty(
            tbl_name,
            "delta.enableRowTracking",
            str(self._tbl_properties["row_tracking"]).lower(),
        )
        self._set_delta_tblproperty(
            tbl_name,
            "delta.enableTypeWidening",
            str(self._tbl_properties["type_widening"]).lower(),
        )
        if self._tbl_properties["tblproperties"]:
            for property, value in self._tbl_properties["tblproperties"].items():
                self._set_delta_tblproperty(tbl_name, property, value)

    def _clusterby(self, tbl_name: str, cols: list[str] | None):
        """Liquid cluster by an existing delta table

        Args:
            tbl_name (str): tbl name uri as catalog.schema.table
            cols (list[str]|None): list of columns to cluster or None to remove clustering
        """
        if cols is None:
            cols = []
        det = self.spark.sql(f"DESCRIBE DETAIL {tbl_name}")
        if det.collect()[0].clusteringColumns != cols:
            cols_str = f"({', '.join(cols)})" if cols else None
            self.spark.sql(f"ALTER TABLE {tbl_name} CLUSTER BY {cols_str}")

    def _set_delta_tblproperty(self, tbl_name: str, property: str, value: str) -> None:
        """Set a delta table property

        Sets the property only if any change is detected.
        Check for properties the docu: https://docs.delta.io/

        Args:
            tbl_name (str): tbl name uri as catalog.schema.table
            property (str): property name
            value (str): property value
        """
        details = self.spark.sql(f"DESCRIBE DETAIL {tbl_name}")
        current_value = details.collect()[0].properties.get(property)
        if current_value != value:
            self.spark.sql(
                f"ALTER TABLE {tbl_name} SET TBLPROPERTIES ('{property}' = '{value}')"
            )
