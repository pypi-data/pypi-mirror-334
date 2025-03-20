from typing import Any, Dict
from lakehouse.daft.etlutils.etlloader import ETLLoader
from lakehouse.daft.etlutils.etltransformer import ETLTransformer
from lakehouse.daft.etlutils.etlwriter import ETLWriter
from lakehouse.daft.etlutils.interface import Interface
from lakehouse.utils import assertion
from lakehouse.utils.lhlogging import log


class ETL(ETLLoader, ETLTransformer, ETLWriter, Interface):
    """A generic class building a framework how to process data from one layer to the other in a Medallion architecture.

    Use the functions load(), transform() and write() to specify configs. Use execute() to execute the defined steps.

    Overwrite functions as required:
        - custom_load(self, table: str) -> daft.DataFrame: Function to customize the way or the source data is loaded. required, if load(mode="custom") else ignored.
        - custom_filter(self, df: daft.DataFrame, table: str) -> daft.DataFrame: Function to filter the loaded dataframe and making use of predicate pushdown. required, if load(filter="custom") else ignored.
        - custom_transform(self, df: daft.DataFrame, table: str) -> daft.DataFrame: Function to be optionally overwritten to add custom transformations, only executed if transform() is defined
        - rename_columns(self, df: daft.DataFrame, table: str) -> daft.DataFrame:
        - select_columns(self, df: daft.DataFrame, table: str) -> daft.DataFrame:
        - cast_column_types(self, df: daft.DataFrame, table: str) -> daft.DataFrame: Function to cast column types based on defined config. Can be overwritten.
        - default_transform(self, df: daft.DataFrame, table: str) -> daft.DataFrame: Can be overwritten to add default transformations executed after the the custom transformations. Defaults create a timestamp column with the current timestamp of transformations. Only executed if transform(ignore_defaults=False)
        - get_replace_condition(self, df: daft.DataFrame, table: str) -> str: Allows you to define the filter used for the replace where overwrite operation. required if write(mode="replace").
        - get_delta_merge_builder(self, df: daft.DataFrame, delta_table: DeltaTable) -> DeltaMergeBuilder: Allows you to define the merge builder for the merge write into delta. required if write(mode="merge")
        - custom_write(self, df: daft.DataFrame, table: str) -> None: Allows to define a custom write operation. required if write(mode="custom")
        - source_path(self, table: str) -> str: Allows you to specify a dynamic path for the target
        - target_path(self, table: str) -> str: Allows you to specify a dynamic path for the target


    Attributes:
        options (Dict[str, Any]): Kwargs, Any options provided into the class
        catalog (str): Name of the catalog, required
        source_schema (str): Name of the source_schema
        target_schema (str): Name of the target_schema
        data (Dict[str, daft.DataFrame]): Intermediate DataFrame per table based on the specified options before execute()
    """

    def __init__(
        self,
        catalog: str,
        source_schema: str,
        target_schema: str,
        config: Dict[str, Any] | None = None,
        **options: Dict[str, Any],
    ) -> None:
        """Initializes the ETL class with user-provided options.

        Args:
            catalog (str): Name of the catalog, required
            source_schema (str): Name of the source_schema, required
            target_schema (str): Name of the target_schema, required
            config (Dict[str, Any] | None): config to optionally pass the configs here instead of passing it during execute. Keys are load, transform, write, optimize and tblproperties
            **options (Dict[str, Any]): Kwargs, Any other options provided into the class
        """
        Interface.__init__(self, catalog, source_schema, target_schema, **options)
        self._load_opts = {"exec": False}
        self._transform_opts = {"exec": False}
        self._write_opts = {"exec": False}
        self.data = {}

        if config:
            self._set_config(config)

    def _set_config(self, config: Dict[str, Any]):
        """Set configs manually if defined

        Args:
            config (Dict[str, Any]): config to optionally pass the configs here instead of passing it during execute. Keys are load, transform, write, optimize and tblproperties
        """
        assertion.assert_allowed_opts(
            config, ["load", "transform", "write", "tblproperties", "optimize"]
        )
        if "load" in config:
            self._load_with_opts(config.get("load"))
        if "transform" in config:
            self._transform_with_opts(config.get("transform"))
        if "write" in config:
            self._write_with_opts(config.get("write"))

    @log("execute", 1)
    def _execute_one(self, table: str) -> None:
        """Orchestrates the etl process for the specified table loading ,transforming and writing the data.

        Load needs to be always defined except for optimize. Assure if running optimize that a write had been execute once to create the table.

        Executes overwrite functions in the following order:
            1. load
            2. transform if transform() specified
            3. write if write() specified

        Args:
            table (str): name of the table

        Raises:
            Exception if no load is specified as this is required
        """
        assertion.assert_execute_options(
            self._load_opts.get("exec"),
            self._transform_opts.get("exec"),
            self._write_opts.get("exec"),
            False,
            False,
        )
        if self._load_opts.get("exec") is True:
            self.data[table] = self._load(table)
        if self._transform_opts.get("exec") is True:
            self.data[table] = self._transform(self.data[table], table)
        if self._write_opts.get("exec") is True:
            self._write(self.data[table], table)

    def execute(self, *tables) -> None:
        """Executes the elt process via _execute_one() for one or multiple tables as specified.

        Args:
            *tables: List of tables as args
        """
        for t in tables:
            self._execute_one(t)
