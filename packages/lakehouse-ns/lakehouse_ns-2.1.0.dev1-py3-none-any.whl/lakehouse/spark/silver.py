from lakehouse.spark.etl import ETL
from pyspark.sql import functions as F
from pyspark.sql import SparkSession, DataFrame
from typing import Any, Dict
from lakehouse.utils import assertion


class Silver(ETL):
    """A generic class building a framework how to process data in the Silver layer in a Medallion architecture.

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
        source_schema (str): Name of the source_schema
        target_schema (str): Name of the target_schema
        data (Dict[str, DataFrame]): Intermediate DataFrame per table based on the specified options before execute()
    """

    def __init__(
        self,
        spark: SparkSession,
        catalog: str,
        source_schema: str,
        target_schema: str,
        config: Dict[str, Any] | None = None,
        **options: Dict[str, Any],
    ) -> None:
        """Initializes the Silver class with user-provided options.

        Args:
            spark (SparkSession): existing Spark Session
            catalog (str): Name of the created catalog recognized by spark e.g. from Hive Metastore or Unity Catalogue, required
            source_schema (str): Name of the source_schema, required
            target_schema (str): Name of the target_schema, required
            config (Dict[str, Any] | None): config to optionally pass the configs here instead of passing it during execute. Keys are load, transform, write, optimize and tblproperties
            **options (Dict[str, Any]): Kwargs, Any other options provided into the class
        """
        super().__init__(
            spark, catalog, source_schema, target_schema, config, **options
        )

    def _load_with_opts(self, opts: Dict[str, Any] | None = None) -> None:
        """Function to assert allowed load options and set them.

        Args:
            opts (Dict[str, Any] | None): load options
        """
        if opts:
            assertion.assert_allowed_opts(opts, ["mode", "filter", "date_col"])
            self.load(**opts)
        else:
            self.load()

    def load(self, mode: str = "default", filter: str = "all", date_col: str = None):
        """Function to set the loader configs.

        Args:
            mode (str): default or custom, default: default, Mode of loading loads either the table from source_schema.table as default or as defined in the custom_load function. In Bronze always a custom_load function is needed meaning the default is custom
            filter (str): all or custom, default: all, Allows applying directly filters on the loaded data for predicate pushdown using "custom", otherwise "all" data is loaded. In Bronze always all data is loaded based on the custom_load function
            date_col (str): Name of the date column used to determine new data, default: None, must exist in the source and target schema and must be defined if filter is new

        Returns:
            self
        """
        options = {"mode": mode, "filter": filter, "date_col": date_col}
        assertion.assert_load_options(options)
        # options: default, custom
        self._load_opts["mode"] = mode
        # options: all, custom (later new)
        self._load_opts["filter"] = filter
        self._load_opts["date_col"] = date_col
        # options: always None as in Silver source tbl name equals target
        self._load_opts["source_tbl"] = None
        self._load_opts["exec"] = True
        return self

    def default_transform(self, df: DataFrame, table: str) -> DataFrame:
        """Function adding the current timestamp as LH_SilverTS to the transformed data.

        Can be overwritten if more internal transformations should be added

        Args:
            df (DataFrame): DataFrame
            table (str): name of the table

        Returns:
            transformed DataFrame with internal transformations
        """
        cols = df.columns
        t = {"LH_SilverTS": F.current_timestamp()}
        df = df.withColumns(t)
        return df.select("LH_SilverTS", *cols)
