from typing import Any, Dict
from lakehouse.utils import assertion
from lakehouse.daft.etlutils.interface import Interface
from lakehouse.utils import lhlogging
from lakehouse.daft.utils import daftutils
import datetime as dt
import daft


class ETLTransformer(Interface):
    """A generic class integrating the transformation of data.

    Use the function transform to set the transform configs. Use _transform() to execute the transform process.

    Overwrite functions as required:
        - custom_transform(self, df: daft.DataFrame, table: str) -> daft.DataFrame: Function to be optionally overwritten to add custom transformations, only executed if transform() is defined
        - rename_columns(self, df: daft.DataFrame, table: str) -> daft.DataFrame:
        - select_columns(self, df: daft.DataFrame, table: str) -> daft.DataFrame:
        - cast_column_types(self, df: daft.DataFrame, table: str) -> daft.DataFrame: Function to cast column types based on defined config. Can be overwritten.
        - default_transform(self, df: daft.DataFrame, table: str) -> DataFrame: Can be overwritten to add default transformations executed after the the custom transformations. Defaults create a timestamp column with the current timestamp of transformations. Only executed if transform(ignore_defaults=False)

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
        """Initializes the Transformer class with user-provided options.

        Args:
            catalog (str): Name of the catalog, required
            source_schema (str): Name of the source_schema, required
            target_schema (str): Name of the target_schema, required
            **options (Dict[str, Any]): Kwargs, Any other options provided into the class
        """
        Interface.__init__(self, catalog, source_schema, target_schema, **options)
        self._transform_opts = {"exec": False}

    def _transform_with_opts(self, opts: Dict[str, Any] | None = None) -> None:
        """Function to assert allowed transform options and set them.

        Args:
            options (Dict[str, Any] | None): transform options
        """
        if opts:
            assertion.assert_allowed_opts(
                opts,
                [
                    "ignore_defaults",
                    "transformation_order",
                    "tbl_transformations",
                    "rename_columns",
                    "select_columns",
                    "cast_column_types",
                ],
            )
            self.transform(**opts)
        else:
            self.transform()

    def transform(
        self,
        ignore_defaults: bool = False,
        transformation_order: list[str] = [
            "rename_columns",
            "tbl_transformations",
            "select_columns",
            "cast_column_types",
        ],
        tbl_transformations: Dict[str, str] = {},
        rename_columns: Dict[str, Dict[str, str]] = {},
        select_columns: Dict[str, list[str]] = {},
        cast_column_types: Dict[str, Dict[str, str]] = {},
    ):
        """Function to set the transformer configs.

        Args:
            ignore_defaults (bool): default: False, Ignores executing default transformations as defined in default_transform function if True. Usually used during debugging
            transformation_order (List[str]): default: ["rename_columns", "tbl_transformations", "select_columns", "cast_column_types"], Allows to define the order of transformations to be executed. Default is
            tbl_transformations (Dict[str, str]): default: {}, Allows to define custom transformations per table by specifying the table name as key and the function name as value. For the tables it is not defined custom_transform is used.
            rename_columns (Dict[str, Dict[str, str]]): default: {}, Allows to define column renaming per table by specifying the table name as key and the column renaming as value. The value is a dictionary with the old column name as key and the new column name as value.
            select_columns (Dict[str, list[str]]): default: {}, Allows to define column selection per table by specifying the table name as key and the column names as value.
            cast_column_types (Dict[str, Dict[str, str]]): default: {}, Allows to define column casting per table by specifying the table name as key and the column casting as value. The value is a dictionary with the column name as key and the cast type as value.

        Returns:
            self
        """
        options = {
            "ignore_defaults": ignore_defaults,
            "transformation_order": transformation_order,
            "tbl_transformations": tbl_transformations,
            "rename_columns": rename_columns,
            "select_columns": select_columns,
            "cast_column_types": cast_column_types,
        }
        assertion.assert_transform_options(options, self)
        assertion.assert_transform_functions(self, transformation_order)

        for option, value in options.items():
            self._transform_opts[option] = value
        self._transform_opts["exec"] = True
        return self

    @lhlogging.log("transform", 2)
    def _transform(self, df: daft.DataFrame, table: str) -> daft.DataFrame:
        """Function orchestrating the trasnsform based on the transform_opts.

        Executes transformations based on transformation_order and afterwords default_transform if ignore_defaults = False.
        Otherwise only custom_transform is executed
        Custom transformations can be defined per table in tbl_transformations. For the tables it is not defined custom_transform is used.
        For the custom tbl_transformations the list element tbl_transformations is replaced with the custom function.

        Args:
            df (daft.DataFrame): DataFrame
            table (str): name of the table

        Returns:
            transformed DataFrame
        """
        func_list = self._transform_opts["transformation_order"]
        f = self._transform_opts["tbl_transformations"].get(table, "custom_transform")
        func_list = [f if e == "tbl_transformations" else e for e in func_list]
        for func in func_list:
            df = getattr(self, func)(df, table)
        if not self._transform_opts["ignore_defaults"]:
            df = self.default_transform(df, table)
        return df

    def custom_transform(self, df: daft.DataFrame, table: str) -> daft.DataFrame:
        """Function to be optionally overwritten to add custom transformations, only executed if transform() is defined

        Args:
            df (daft.DataFrame): DataFrame
            table (str): name of the table

        Returns:
            transformed DataFrame
        """
        return df

    def rename_columns(self, df: daft.DataFrame, table: str) -> daft.DataFrame:
        """Function to rename columns based on defined config. Can be overwritten.

        Args:
            df (daft.DataFrame): DataFrame
            table (str): name of the table

        Returns:
            transformed DataFrame
        """
        rename_cols: Dict = self._transform_opts.get("rename_columns", {}).get(table)
        if rename_cols:
            df = df.with_columns_renamed(rename_cols)
        return df

    def select_columns(self, df: daft.DataFrame, table: str) -> daft.DataFrame:
        """Function to select columns based on defined config. Can be overwritten.

        Args:
            df (daft.DataFrame): DataFrame
            table (str): name of the table

        Returns:
            transformed DataFrame
        """
        select_cols: list = self._transform_opts.get("select_columns", {}).get(table)
        if select_cols:
            df = df.select(*select_cols)
        return df

    def cast_column_types(self, df: daft.DataFrame, table: str) -> daft.DataFrame:
        """Function to cast column types based on defined config. Can be overwritten.

        Args:
            df (daft.DataFrame): DataFrame
            table (str): name of the table

        Returns:
            transformed DataFrame
        """
        cast_cols: Dict = self._transform_opts.get("cast_column_types", {}).get(table)
        if cast_cols:
            casts = {}
            for col, cast_type in cast_cols.items():
                if col in df.column_names:
                    daft_type = daftutils.get_daft_dtype(cast_type)
                    casts[col] = daft.col(col).cast(daft_type)
            df = df.with_columns(casts)
        return df

    def default_transform(self, df: daft.DataFrame, table: str) -> daft.DataFrame:
        """Can be overwritten to add default transformations executed after the the custom transformations. Defaults create a timestamp column with the current timestamp of transformations. Only executed if transform(ignore_defaults=False)

        Args:
            df (daft.DataFrame): DataFrame
            table (str): name of the table

        Returns:
            transformed DataFrame with internal transformations
        """
        cols = df.columns
        current_timestamp = dt.datetime.now()
        df = df.with_column("LH_TS", daft.lit(current_timestamp))
        return df.select("LH_TS", *cols)
