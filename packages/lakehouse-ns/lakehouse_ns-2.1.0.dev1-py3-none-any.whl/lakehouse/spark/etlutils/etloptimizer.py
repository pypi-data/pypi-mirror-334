from pyspark.sql import SparkSession
from typing import Any, Dict
from lakehouse.utils import assertion
from lakehouse.spark.utils import assertionspark
from lakehouse.spark.etlutils.interface import Interface
from lakehouse.utils.lhlogging import log


class ETLOptimizer(Interface):
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
        """Initializes the Optimizer class with user-provided options.

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
        self._optimize_opts = {"exec": False}

    def _optimize_with_opts(self, opts: Dict[str, Any] | None = None) -> None:
        """Function to assert allowed optimize options and set them.

        Args:
            opts (Dict[str, Any] | None): optimize options
        """
        if opts:
            assertion.assert_allowed_opts(
                opts,
                [
                    "optimize",
                    "optimize_full",
                    "vacuum",
                    "vacuum_lite",
                    "analyze",
                    "retention",
                    "excl_cols",
                ],
            )
            self.optimize(**opts)
        else:
            self.optimize()

    def optimize(
        self,
        optimize: bool = False,
        optimize_full: bool = False,
        vacuum: bool = False,
        vacuum_lite: bool = False,
        analyze: bool = False,
        retention: int | None = None,
        excl_cols: list[str] | None = None,
    ):
        """Function to set the optimize configs.

        Args:
            optimize (bool): execute the optimize command on the given tables
            optimize_full (bool): execute the optimize as Full mode (needs Liquid clustering)
            vacuum (bool): execute the vacuum command on the given tables as to the defined retention
            vacuum_lite (bool): execute the vacuum with lite command
            analyze (bool): execute the analyze command on the given table to compute statistics
            retention (int): retention time for files to be considered for vacuum. Retention time must be at higher or equal default retention threshold. The default is 7 days (168 hours). If no value is provided retention threshold is taken. The threshold can be changed with the delta property delta.deletedFileRetentionDuration
            excl_cols (list[str]): list of cols to be excluded to compute statistics

        Returns:
            self
        """
        options = {
            "optimize": optimize,
            "optimize_full": optimize_full,
            "vacuum": vacuum,
            "vacuum_lite": vacuum_lite,
            "analyze": analyze,
            "retention": retention,
            "excl_cols": excl_cols,
        }
        assertion.assert_optimize_options(options)
        for options, value in options.items():
            self._optimize_opts[options] = value
        self._optimize_opts["exec"] = True
        return self

    @log("optimize", 1)
    def _optimize(self, table: str) -> None:
        """Function orchestrating the obtimize based on the optimize_opts.

        If optimize True execute the optimize
        If vacuum True execute the vacuum with the given retention time or None
        If analyze True execute analyze to compute statistics ignoring any given exluded cols

        Args:
            table (str): name of the table
        """
        tbl_name = f"{self.catalog}.{self.target_schema}.{table}"
        assertionspark.assert_optimize_options_per_tbl(
            self._optimize_opts, self.spark, tbl_name
        )
        if self._optimize_opts["optimize"]:
            self._exec_optimize(tbl_name, self._optimize_opts["optimize_full"])
        if self._optimize_opts["vacuum"]:
            self._exec_vacuum(
                tbl_name,
                self._optimize_opts["vacuum_lite"],
                self._optimize_opts["retention"],
            )
        if self._optimize_opts["analyze"]:
            if self._optimize_opts["excl_cols"]:
                cols = self._get_analyze_cols(
                    tbl_name, self._optimize_opts["excl_cols"]
                )
                self._exec_analyze(tbl_name, cols)
            else:
                self._exec_analyze(tbl_name)

    def _exec_optimize(self, tbl_name: str, full: bool = False):
        """Run the optimize on a given table

        Args:
            tbl_name (str): tbl name uri as catalog.schema.table
            full (bool): executing optimize in full mode
        """
        if full is True:
            self.spark.sql(f"OPTIMIZE {tbl_name} FULL")
        else:
            self.spark.sql(f"OPTIMIZE {tbl_name}")

    def _exec_vacuum(
        self, tbl_name: str, lite=False, retention: int | None = None
    ) -> None:
        """Run vacuum based on given retention time

        Args:
            tbl_name (str): tbl name uri as catalog.schema.table
            retention (int): retention time for files to be considered for vacuum. If not provided retention threshhold which defaults to 7 days is taken
            lite (bool): running vacuum in lite mode
        """
        query = f"VACUUM {tbl_name}"
        if lite is True:
            query = query + " LITE"
        if retention:
            query = query + f" RETAIN {str(retention)} HOURS"
        self.spark.sql(query)

    def _exec_analyze(self, tbl_name: str, cols: list[str] | None = None) -> None:
        """Execute analyze for all columns or for all given columns

        Args:
            tbl_name (str): tbl name uri as catalog.schema.table
            cols (list[str]|None): columns to compute statistics with analyze
        """

        base_query = f"ANALYZE TABLE {tbl_name} COMPUTE STATISTICS FOR"
        try:
            if cols:
                self.spark.sql(f"{base_query} COLUMNS {', '.join(cols)}")
            else:
                self.spark.sql(f"{base_query} ALL COLUMNS")
        except Exception as error:
            e = f"ANALYZE might not be supported by your chosen spark session or catalog. The following error has been raised: {error}"
            raise Exception(e)

    def _get_analyze_cols(self, tbl_name, excl_cols: list[str]) -> list:
        """Get columns from given table excluding the excluded columns

        Args:
            tbl_name (str): tbl name uri as catalog.schema.table
            cols (list[str]): columns to be excluded

        Returns:
            list of columns filtered by excl_cols
        """
        all_cols = self.spark.table(tbl_name).columns
        return [c for c in all_cols if c not in excl_cols]
