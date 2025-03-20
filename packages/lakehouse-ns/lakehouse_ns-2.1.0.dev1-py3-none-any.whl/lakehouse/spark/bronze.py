from lakehouse.spark.etl import ETL
from pyspark.sql import functions as F
from pyspark.sql import SparkSession, DataFrame
from typing import Any, Dict
from lakehouse.spark.utils import assertionspark


class Bronze(ETL):
    """A generic class building a framework how to process data in the Bronze layer in a Medallion architecture.

    Use the functions load(), transform() and write() to specify configs. Use execute() to execute the defined steps.

    Overwrite functions as required:
        - custom_load(self, table: str) -> DataFrame: Function to customize the way or the source data is loaded. required, if load(mode="custom") else ignored.
        - custom_filter(self, df: DataFrame, table: str) -> DataFrame: Function to filter the loaded dataframe and making use of predicate pushdown. required, if load(filter="custom") else ignored.
        - custom_transform(self, df: DataFrame, table: str) -> DataFrame: Function to be optionally overwritten to add custom transformations, only executed if transform() is defined
        - rename_columns(self, df: DataFrame, table: str) -> DataFrame:
        - select_columns(self, df: DataFrame, table: str) -> DataFrame:
        - cast_column_types(self, df: DataFrame, table: str) -> DataFrame: Function to cast column types based on defined config. Can be overwritten.
        - default_transform(self, df: DataFrame, table: str) -> DataFrame: Can be overwritten to add default transformations executed after the the custom transformations. Defaults create a timestamp column with the current timestamp of transformations. Only executed if transform(ignore_defaults=False)
        - get_replace_condition(self, df: DataFrame, table: str) -> str: Allows you to define the filter used for the replace where overwrite operation. required if write(mode="replace").
        - get_delta_merge_builder(self, df: DataFrame, delta_table: DeltaTable) -> DeltaMergeBuilder: Allows you to define the merge builder for the merge write into delta. required if write(mode="merge")
        - custom_write(self, df: DataFrame, table: str) -> None: Allows to define a custom write operation. required if write(mode="custom")
        - target_path(self, table: str) -> str: Allows you to specify a dynamic path if using external tables
        - checkpoint_path(self, table: str) -> str: Function to be overwritten to create the checkpoint path if performing a streaming write

    Attributes:
        spark (SparkSession): Spark Session as provided to process the data
        options (Dict[str, Any]): Kwargs, Any options provided into the class
        catalog (str): Name of the created catalog recognized by spark e.g. from Hive Metastore or Unity Catalogue
        target_schema (str): Name of the target_schema
        data (Dict[str, DataFrame]): Intermediate DataFrame per table based on the specified options before execute()
    """

    def __init__(
        self,
        spark: SparkSession,
        catalog: str,
        target_schema: str,
        config: Dict[str, Any] | None = None,
        **options: Dict[str, Any],
    ) -> None:
        """Initializes the Bronze class with user-provided options.

        Args:
            spark (SparkSession): existing Spark Session
            catalog (str): Name of the created catalog recognized by spark e.g. from Hive Metastore or Unity Catalogue, required
            target_schema (str): Name of the target_schema, required
            config (Dict[str, Any] | None): config to optionally pass the configs here instead of passing it during execute. Keys are load, transform, write, optimize and tblproperties
            **options (Dict[str, Any] | None): Kwargs, Any options provided into the class
        """
        opts = {"catalog": catalog, "target_schema": target_schema}
        assertionspark.assert_class_options(opts, spark)
        self.spark = spark
        self.catalog = catalog
        spark.catalog.setCurrentCatalog(catalog)
        self.target_schema = target_schema
        self.options = options

        self._load_opts = {"exec": False}
        self._transform_opts = {"exec": False}
        self._write_opts = {"exec": False}
        self._optimize_opts = {"exec": False}
        self._tbl_properties = {"exec": False}
        self.data = {}

        if config:
            self._set_config(config)

    def _load_with_opts(self, opts: Dict[str, Any] | None = None) -> None:
        """Function to assert allowed load options and set them.

        Args:
            opts (Dict[str, Any] | None): load options
        """
        assert opts is None, "No load options allowed in Bronze"
        self.load()

    def load(self):
        """Function to set the loader configs.

        Returns:
            self
        """
        self._load_opts["mode"] = "custom"  # options: always custom as load from source
        self._load_opts["filter"] = "all"  # options: always all as no filter in bronze
        # options: always None as in Bronze source tbl name equals target
        self._load_opts["source_tbl"] = None
        self._load_opts["date_col"] = None
        self._load_opts["exec"] = True
        return self

    def default_transform(self, df: DataFrame, table: str) -> DataFrame:
        """Function adding the current timestamp as LH_BronzeTS to the transformed data.

        Can be overwritten if more internal transformations should be added

        Args:
            df (DataFrame): DataFrame
            table (str): name of the table

        Returns:
            transformed DataFrame with internal transformations
        """
        cols = df.columns
        t = {"LH_BronzeTS": F.current_timestamp()}
        df = df.withColumns(t)
        return df.select("LH_BronzeTS", *cols)
