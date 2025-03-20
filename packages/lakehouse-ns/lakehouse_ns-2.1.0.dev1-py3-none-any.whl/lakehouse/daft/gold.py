from lakehouse.daft.etl import ETL
import daft
from typing import Any, Dict
import datetime as dt
import daft


class Gold(ETL):
    """A generic class building a framework how to process data in the Gold layer in a Medallion architecture.

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
        """Initializes the Gold class with user-provided options.

        Args:
            catalog (str): Name of the catalog, required
            source_schema (str): Name of the source_schema, required
            target_schema (str): Name of the target_schema, required
            config (Dict[str, Any] | None): config to optionally pass the configs here instead of passing it during execute. Keys are load, transform, write, optimize and tblproperties
            **options (Dict[str, Any]): Kwargs, Any other options provided into the class
        """
        super().__init__(catalog, source_schema, target_schema, config, **options)

    def default_transform(self, df: daft.DataFrame, table: str) -> daft.DataFrame:
        """Function adding the current timestamp as LH_GoldTS to the transformed data.

        Can be overwritten if more internal transformations should be added

        Args:
            df (daft.DataFrame): DataFrame
            table (str): name of the table

        Returns:
            transformed DataFrame with internal transformations
        """
        cols = df.columns
        current_timestamp = dt.datetime.now()
        df = df.with_column("LH_GoldTS", daft.lit(current_timestamp))
        return df.select("LH_GoldTS", *cols)
