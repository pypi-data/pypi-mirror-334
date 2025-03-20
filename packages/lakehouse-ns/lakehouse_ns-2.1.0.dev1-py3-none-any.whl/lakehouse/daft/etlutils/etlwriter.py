import daft
from typing import Any, Dict, Literal
from deltalake.table import TableMerger, DeltaTable
from lakehouse.utils import assertion
from lakehouse.daft.etlutils.interface import Interface
from lakehouse.utils import lhlogging
from lakehouse.daft.utils import deltarsutils
import deltalake
import pyarrow


class ETLWriter(Interface):
    """A generic class integrating the writing of data.

    Use the function write to set the write configs. Use _write() to execute the writing process.

    Overwrite functions as required:
        - get_replace_condition(self, df: daft.DataFrame, table: str) -> str: Allows you to define the filter used for the replace where overwrite operation. required if write(mode="replace").
        - get_delta_merge_builder(self, df: daft.DataFrame, delta_table: DeltaTable) -> DeltaMergeBuilder: Allows you to define the merge builder for the merge write into delta. required if write(mode="merge")
        - custom_write(self, df: daft.DataFrame, table: str) -> None: Allows to define a custom write operation. required if write(mode="custom")
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
        """Initializes the Writer class with user-provided options.

        Args:
            catalog (str): Name of the catalog, required
            source_schema (str): Name of the source_schema, required
            target_schema (str): Name of the target_schema, required
            **options (Dict[str, Any]): Kwargs, Any other options provided into the class
        """
        Interface.__init__(self, catalog, source_schema, target_schema, **options)
        self._write_opts = {"exec": False}

    def _write_with_opts(self, opts: Dict[str, Any] | None = None) -> None:
        """Function to assert allowed write options and set them.

        Args:
            opts (Dict[str, Any] | None): write options
        """
        if opts:
            assertion.assert_allowed_opts(opts, ["mode", "overwrite_schema"])
            self.write(**opts)
        else:
            self.write()

    def write(
        self,
        mode: Literal["overwrite", "append", "replace", "merge", "custom"] = "append",
        overwrite_schema: bool = False,
    ):
        """Function to set the writer configs.

        Args:
            mode (str): overwrite, append, replace, merge or custom, default: append, Defines the mode of writing the data as overwrite, append, replace (define replace filter with function get_replace_condition(), merge (define merge builder with function get_delta_merge_builder(), custom (define custom_write() function)
            overwrite_schema (bool): True if schema should be overwritten, default: False, only available for mode overwrite

        Returns:
            self
        """
        options = {"mode": mode, "overwrite_schema": overwrite_schema}
        assertion.assert_write_options(options)
        # overwrite, append, replace, merge, custom (later scd2, Stream)
        for option, value in options.items():
            self._write_opts[option] = value
        self._write_opts["exec"] = True
        return self

    @lhlogging.log("write", 2)
    def _write(self, df: daft.DataFrame, table: str) -> None:
        """Function orchestrating the write based on the write_opts.

        - mode=overwrite executes _overwrite(),
        - mode=append executes _append(),
        - mode=replace executes _replace() and requires get_replace_condition() to be defined,
        - mode=merge executes _merge() and requires get_delta_merge_builder() to be defined
        - mode=custom executes custom_write() and needs this function to be defined

        Args:
            df (daft.DataFrame): DataFrame
            table (str): name of the table
        """

        func_dict = {
            "overwrite": self._overwrite,
            "append": self._append,
            "replace": self._replace,
            "merge": self._merge,
            "custom": self.custom_write,
        }
        func_dict[self._write_opts["mode"]](df, table)

    def target_path(self, table: str) -> str:
        """Function to be overwritten to create the table path.

        Create a string depending e.g. on catalog, env, schema and table

        Example:
            >>> return f"D:/Data/{self.catalog}/{self.target_schema}/{table}"

        Args:
            table (str): name of the table

        Return:
            Path depening on table and other variables
        """
        e = "Function 'def target_path(self, table: str) -> str:' needs to be implemented if write(tbl_type=external)"
        raise NotImplementedError(e)

    # TODO: in writer maybe write as functions to be re-usable
    def _overwrite(self, df: daft.DataFrame, table: str) -> None:
        """Overwrites the data on the targeting table.

        Executes an overwrite schema if merge_schema = True

        Args:
            df (daft.DataFrame): DataFrame
            table (str): name of the table
        """
        if self._write_opts["overwrite_schema"] is True:
            schema_mode = "overwrite"
        else:
            schema_mode = None
        df.write_deltalake(
            self.target_path(table), mode="overwrite", schema_mode=schema_mode
        )

    def _append(self, df: daft.DataFrame, table: str) -> None:
        """Appends the data on the targeting table.

        Executes a merge_schema if merge_schema = True.

        Args:
            df (daft.DataFrame): DataFrame
            table (str): name of the table
        """
        df.write_deltalake(self.target_path(table), mode="append")

    def get_replace_condition(self, df: daft.DataFrame, table: str) -> str:
        """Condition as SQL expression to overwrite specific data.

        Input data has to fullfill this condition

        Example:
            >>> return "sample_col >= sample_value"

        Args:
            df (daft.DataFrame): DataFrame
            table (str): name of the table
        """
        e = "Function 'def get_replace_condition(self, df: daft.DataFrame, table: str) -> str:' needs to be implemented if write(mode=replace)"
        raise NotImplementedError(e)

    def _replace(self, df: daft.DataFrame, table: str) -> None:
        """Overwrite data based on a provided condition in get_replace_condition() using replaceWhere

        Executes a merge_schema if merge_schema = True.

        Args:
            df (daft.DataFrame): DataFrame
            table (str): name of the table
        """
        deltalake.write_deltalake(
            self.target_path(table),
            df.to_arrow(),
            mode="overwrite",
            predicate=self.get_replace_condition(df, table),
        )

    def get_delta_merge_builder(
        self, df: pyarrow.Table, delta_table: DeltaTable
    ) -> TableMerger:
        """Abstract function to define a DeltaMergeBuilder to perform the merge in the write function.

        Executes a merge_schema if merge_schema = True.

        Example:
            >>> merge_condition = "target.primary_key = source.primary_key"
            >>> builder = delta_table.merge(df, predicate=merge_condition, source_alias="source", target_alias="target")
            >>> builder = builder.when_matched_update_all()
            >>> builder = builder.when_not_matched_insert_all()
            >>> return builder

        More examples can be found here: https://delta-io.github.io/delta-rs/api/delta_table/delta_table_merger/

        Args:
            df (pyarrow.Table): DataFrame as pyarrow table to be written
            delta_table (DeltaTable): target delta table to write to
        """

        e = "Function 'def get_delta_merge_builder(self, df: pyarrow.Table, delta_table: DeltaTable) -> TableMerger:' needs to be implemented if write(mode=merge)"
        raise NotImplementedError(e)

    def _merge(self, df: daft.DataFrame, table: str) -> None:
        """Merges data based on a defined delta_merge_builder in get_delta_merge_builder().

        Args:
            df (daft.DataFrame): DataFrame
            table (str): name of the table
        """
        if deltarsutils.delta_table_exists(self.target_path(table)):
            delta_table = DeltaTable(self.target_path(table))
            merge_builder = self.get_delta_merge_builder(df.to_arrow(), delta_table)
            merge_builder.execute()
        else:
            df.write_deltalake(self.target_path(table), mode="overwrite")

    def custom_write(self, df: daft.DataFrame, table: str) -> None:
        """Abstract function to write a DataFrame.

        Args:
            df (daft.DataFrame): DataFrame
            table (str): name of the table
        """
        e = "Function 'def custom_write(self, df: daft.DataFrame, table: str) -> None:' needs to be implemented if write(mode=custom)"
        raise NotImplementedError(e)
