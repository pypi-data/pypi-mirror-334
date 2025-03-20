import daft
from typing import Any, Dict, Literal
from lakehouse.daft.utils import assertiondaft, deltarsutils
from lakehouse.daft.etlutils.interface import Interface
from lakehouse.utils import assertion
from lakehouse.utils import lhlogging


class ETLLoader(Interface):
    """A generic class integrating the loading of data.

    Use the function load to set the loader configs. Use _load() to execute the loading process.

    Overwrite functions as required:
        - custom_load(self, table: str) -> daft.DataFrame: Function to customize the way or the source data is loaded. required, if load(mode="custom") else ignored.
        - custom_filter(self, df: daft.DataFrame, table: str) -> daft.DataFrame: Function to filter the loaded dataframe and making use of predicate pushdown. required, if load(filter="custom") else ignored.
        - source_path(self, table: str) -> str: Allows you to specify a dynamic path for the source
        - target_path(self, table: str) -> str: Allows you to specify a dynamic path for the target

    Attributes:
        options (Dict[str, Any]): Kwargs, Any options provided into the class
        catalog (str): Name of the catalog, required
        source_schema (str): Name of the source_schema
        target_schema (str): Name of the target_schema
    """

    def __init__(
        self,
        catalog: str,
        source_schema: str,
        target_schema: str,
        **options: Dict[str, Any],
    ) -> None:
        """Initializes the Loader class with user-provided options.

        Args:
            catalog (str): Name of the catalog, required
            source_schema (str): Name of the source_schema, required
            target_schema (str): Name of the target_schema, required
            **options (Dict[str, Any]): Kwargs, Any other options provided into the class
        """
        Interface.__init__(self, catalog, source_schema, target_schema, **options)
        self._load_opts = {"exec": False}

    def _load_with_opts(self, opts: Dict[str, Any] | None = None) -> None:
        """Function to assert allowed load options and set them.

        Args:
            opts (Dict[str, Any] | None): load options
        """
        if opts:
            assertion.assert_allowed_opts(
                opts, ["mode", "filter", "date_col", "source_tbl"]
            )
            self.load(**opts)
        else:
            self.load()

    def load(
        self,
        mode: Literal["default", "custom"] = "default",
        filter: Literal["all", "custom", "new"] = "all",
        date_col: str | None = None,
        source_tbl: str | None = None,
    ):
        """Function to set the loader configs.

        Args:
            mode (str): default or custom, default: default, Mode of loading loads either the table from source_schema.table as default or as defined in the custom_load function. In Bronze always a custom_load function is needed meaning the default is custom
            filter (str): all, custom or new, default: all, Allows applying directly filters on the loaded data for predicate pushdown using "custom", otherwise "all" data is loaded. New determines based on a datae column which data is new. In Bronze always all data is loaded based on the custom_load function
            date_col (str): Name of the date column used to determine new data, default: None, must exist in the source and target schema and must be defined if filter is new
            source_tbl (str): Name of the source table, default: None, If provided the source table is used instead of the provided target table to load data

        Returns:
            self
        """
        options = {
            "mode": mode,
            "filter": filter,
            "date_col": date_col,
            "source_tbl": source_tbl,
        }
        assertion.assert_load_options(options)
        # options for mode: default, custom
        # options for filter: all, custom, new
        for option, value in options.items():
            self._load_opts[option] = value
        self._load_opts["exec"] = True
        return self

    @lhlogging.log("load", 1)
    def _load(self, table: str) -> daft.DataFrame:
        """Function orchestrating the load based on the load_opts.

        If source_tbl provided use this table name else use the input table name.
        If mode is default call _default_load() else call custom_load().
        If filter is all return the loaded data else call custom_filter() an return the result.

        Args:
            table (str): name of the table

        Returns:
            loaded/filtered data as DataFrame
        """
        if self._load_opts["source_tbl"]:
            table = self._load_opts["source_tbl"]

        if self._load_opts["mode"] == "default":
            df = self._default_load(table)
        elif self._load_opts["mode"] == "custom":
            df = self.custom_load(table)

        if self._load_opts["filter"] == "all":
            return df
        elif self._load_opts["filter"] == "custom":
            return self.custom_filter(df, table)
        elif self._load_opts["filter"] == "new":
            return self._filter_new_data(df, table)

    def source_path(self, table: str) -> str:
        """Function to be overwritten to create the table path.

        Create a string depending e.g. on catalog, env, schema and table

        Example:
            >>> return f"D:/Data/{self.catalog}/{self.source_schema}/{table}"

        Args:
            table (str): name of the table

        Return:
            Path depening on table and other variables
        """
        e = "Function 'def source_path(self, table: str) -> str:' needs to be implemented if write(tbl_type=external)"
        raise NotImplementedError(e)

    def target_path(self, table: str) -> str:
        """Function to be overwritten to create the table path.

        Create a string depending e.g. on catalog, env, schema and table

        Example:
            >>> return f"D:{self.catalog}/{self.target_schema}/{table}"

        Args:
            table (str): name of the table

        Return:
            Path depening on table and other variables
        """
        e = "Function 'def target_path(self, table: str) -> str:' needs to be implemented if write(tbl_type=external)"
        raise NotImplementedError(e)

    def _default_load(self, table: str) -> daft.DataFrame:
        """Function to load data from source_schema.table and return a DataFrame

        Args:
            table (str): name of the table

        Returns:
            loaded data as DataFrame
        """
        return daft.read_deltalake(self.source_path(table))

    def custom_load(self, table: str) -> daft.DataFrame:
        """Abstract function to be overwritten to load data based on custom implemenatation and return a DataFrame

        Args:
            table (str): name of the table

        Returns:
            loaded data as DataFrame
        """
        e = "Function 'def custom_load(self, table: str) -> daft.DataFrame:' needs to be implemented if load(mode=custom)"
        raise NotImplementedError(e)

    def custom_filter(self, df: daft.DataFrame, table: str) -> daft.DataFrame:
        """Abstract function which can be overwritten to filter the loaded dataframe and making use of predicate pushdown.

        Filter rows and columns not needed here before applying any other transformations in transform()

        Args:
            df (daft.DataFrame): DataFrame
            table (str): name of the table

        Returns:
            filtered DataFrame
        """
        e = "Function 'def custom_filter(self, df: daft.DataFrame, table: str) -> daft.DataFrame:' needs to be implemented if load(filter=custom)"
        raise NotImplementedError(e)

    def _filter_new_data(self, df: daft.DataFrame, table: str) -> daft.DataFrame:
        """Function to filter the loaded dataframe and making use of predicate pushdown.

        Filters out only newly added data

        Args:
            df (daft.DataFrame): DataFrame
            table (str): name of the table

        Returns:
            filtered DataFrame
        """
        date_col = self._load_opts["date_col"]
        if deltarsutils.delta_table_exists(self.target_path(table)):
            df_target = daft.read_deltalake(self.target_path(table))
            if df_target.count_rows() > 0:
                assertiondaft.assert_col_in_dataframe(df_target, date_col)
                max_timestamp = df_target.max(date_col).to_pydict()[date_col][0]
                df = df.where(daft.col(date_col) > max_timestamp)
        return df
