from pyspark.sql import SparkSession, DataFrame
from typing import Any, Dict, Literal
from delta.tables import DeltaMergeBuilder, DeltaTable
from lakehouse.utils import assertion
from lakehouse.spark.etlutils.interface import Interface
from lakehouse.utils.lhlogging import log


class ETLWriter(Interface):
    """A generic class integrating the writing of data.

    Use the function write to set the write configs. Use _write() to execute the writing process.

    Overwrite functions as required:
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
    """

    def __init__(
        self,
        spark: SparkSession,
        catalog: str,
        source_schema: str,
        target_schema: str,
        **options: Dict[str, Any],
    ) -> None:
        """Initializes the Writer class with user-provided options.

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
        self._write_opts = {"exec": False}

    def _write_with_opts(self, opts: Dict[str, Any] | None = None) -> None:
        """Function to assert allowed write options and set them.

        Args:
            opts (Dict[str, Any] | None): write options
        """
        if opts:
            assertion.assert_allowed_opts(opts, ["mode", "merge_schema", "external"])
            self.write(**opts)
        else:
            self.write()

    def write(
        self,
        mode: Literal[
            "overwrite", "append", "replace", "merge", "stream", "custom"
        ] = "append",
        merge_schema: bool = False,
        external: bool = False,
    ):
        """Function to set the writer configs.

        Args:
            mode (str): overwrite, append, replace, merge or custom, default: append, Defines the mode of writing the data as overwrite, append, replace (define replace filter with function get_replace_condition(), merge (define merge builder with function get_delta_merge_builder(), stream (requires checkpoint_path() function), custom (define custom_write() function)
            merge_schema (bool): default: False, If the schema should be automatically envolved/merged
            external (bool): default: False, if True tables are saved as external tables based on the defined path in the path function

        Returns:
            self
        """
        options = {"mode": mode, "merge_schema": merge_schema, "external": external}
        assertion.assert_write_options(options)
        # overwrite, append, replace, merge, custom (later scd2, Stream)
        for option, value in options.items():
            self._write_opts[option] = value
        self._write_opts["exec"] = True
        return self

    @log("write", 2)
    def _write(self, df: DataFrame, table: str) -> None:
        """Function orchestrating the write based on the write_opts.

        - mode=overwrite executes _overwrite(),
        - mode=append executes _append(),
        - mode=replace executes _replace() and requires get_replace_condition() to be defined,
        - mode=merge executes _merge() and requires get_delta_merge_builder() to be defined
        - mode=stream executes _stream()
        - mode=custom executes custom_write() and needs this function to be defined

        Args:
            df (DataFrame): DataFrame
            table (str): name of the table
        """

        func_dict = {
            "overwrite": self._overwrite,
            "append": self._append,
            "replace": self._replace,
            "merge": self._merge,
            "stream": self._stream,
            "custom": self.custom_write,
        }
        func_dict[self._write_opts["mode"]](df, table)

    def target_path(self, table: str) -> str:
        """Function to be overwritten to create the table path.

        Create a string depending e.g. on catalog, env, schema and table

        Example:
            >>> return f"D:/Data/{self.target_schema}/{table}"

        Args:
            table (str): name of the table

        Return:
            Path depening on table and other variables
        """
        e = "Function 'def target_path(self, table: str) -> str:' needs to be implemented if write(tbl_type=external)"
        raise NotImplementedError(e)

    def checkpoint_path(self, table: str) -> str:
        """Function to be overwritten to create the checkpoint path if performing a streaming write.

        Create a string depending e.g. on catalog, env, schema and table

        Example:
            >>> return f"D:/Data/{self.target_schema}/{table}/checkpoint"

        Args:
            table (str): name of the table

        Return:
            Path depening on table and other variables
        """
        e = "Function 'def checkpoint_path(self, table: str) -> str:' needs to be implemented if write(mode=stream)"
        raise NotImplementedError(e)

    # TODO: in writer maybe write as functions to be re-usable
    def _overwrite(self, df: DataFrame, table: str) -> None:
        """Overwrites the data on the targeting table.

        Executes an overwrite schema if merge_schema = True

        Args:
            df (DataFrame): DataFrame
            table (str): name of the table
        """
        tbl_name = f"{self.target_schema}.{table}"
        ops = {
            "overwriteSchema": (
                "true" if self._write_opts["merge_schema"] is True else "false"
            )
        }
        if self._write_opts["external"] is True:
            ops["path"] = self.target_path(table)
        df.write.format("delta").options(**ops).mode("overwrite").saveAsTable(tbl_name)

    def _append(self, df: DataFrame, table: str) -> None:
        """Appends the data on the targeting table.

        Executes a merge_schema if merge_schema = True.

        Args:
            df (DataFrame): DataFrame
            table (str): name of the table
        """
        tbl_name = f"{self.target_schema}.{table}"
        ops = {
            "mergeSchema": (
                "true" if self._write_opts["merge_schema"] is True else "false"
            )
        }
        if self._write_opts["external"] is True:
            ops["path"] = self.target_path(table)
        df.write.format("delta").options(**ops).mode("append").saveAsTable(tbl_name)

    def get_replace_condition(self, df: DataFrame, table: str) -> str:
        """Condition as SQL expression to overwrite specific data.

        Input data has to fullfill this condition

        Example:
            >>> return "sample_col >= sample_value"

        Args:
            df (DataFrame): DataFrame
            table (str): name of the table
        """
        e = "Function 'def get_replace_condition(self, df: DataFrame, table: str) -> str:' needs to be implemented if write(mode=replace)"
        raise NotImplementedError(e)

    def _replace(self, df: DataFrame, table: str) -> None:
        """Overwrite data based on a provided condition in get_replace_condition() using replaceWhere

        Executes a merge_schema if merge_schema = True.

        Args:
            df (DataFrame): DataFrame
            table (str): name of the table
        """
        tbl_name = f"{self.target_schema}.{table}"
        ops = {
            "replaceWhere": self.get_replace_condition(df, table),
            "mergeSchema": (
                "true" if self._write_opts["merge_schema"] is True else "false"
            ),
        }
        if self._write_opts["external"] is True:
            ops["path"] = self.target_path(table)
        df.write.format("delta").options(**ops).mode("overwrite").saveAsTable(tbl_name)

    def _stream(self, df: DataFrame, table: str) -> None:
        ops = {
            "checkpointLocation": self.checkpoint_path(table),
            "mergeSchema": (
                "true" if self._write_opts["merge_schema"] is True else "false"
            ),
        }
        if self._write_opts["external"] is True:
            ops["path"] = self.target_path(table)
        (
            df.writeStream.format("delta")
            .options(**ops)
            .trigger(availableNow=True)
            .outputMode("append")
            .toTable(f"{self.target_schema}.{table}")
            .awaitTermination()
        )

    def get_delta_merge_builder(
        self, df: DataFrame, delta_table: DeltaTable
    ) -> DeltaMergeBuilder:
        """Abstract function to define a DeltaMergeBuilder to perform the merge in the write function.

        Executes a merge_schema if merge_schema = True.

        Example:
            >>> merge_condition = "target.primary_key = source.primary_key"
            >>> builder = delta_table.alias("target").merge(df.alias("source"), merge_condition)
            >>> builder = builder.whenMatchedUpdateAll()
            >>> builder = builder.whenNotMatchedInsertAll()
            >>> return builder

        More examples can be found here: https://docs.delta.io/latest/delta-update.html and https://docs.delta.io/latest/api/python/spark/index.html

        Args:
            df (DataFrame): DataFrame to be written
            delta_table (DeltaTable): target delta table to write to
        """

        e = "Function 'def get_delta_merge_builder(self, df: DataFrame, delta_table: DeltaTable) -> DeltaMergeBuilder:' needs to be implemented if write(mode=merge)"
        raise NotImplementedError(e)

    def _merge(self, df: DataFrame, table: str) -> None:
        """Merges data based on a defined delta_merge_builder in get_delta_merge_builder().

        Args:
            df (DataFrame): DataFrame
            table (str): name of the table
        """
        tbl_name = f"{self.target_schema}.{table}"
        if self.spark.catalog.tableExists(tbl_name):
            delta_table = DeltaTable.forName(self.spark, tbl_name)
            merge_builder = self.get_delta_merge_builder(df, delta_table)
            if self._write_opts["merge_schema"] is True:
                merge_builder = merge_builder.withSchemaEvolution()
            merge_builder.execute()
        else:
            writer = df.write.format("delta").mode("overwrite")
            if self._write_opts["external"] is True:
                writer.option("path", self.target_path(table))
            writer.saveAsTable(tbl_name)

    def custom_write(self, df: DataFrame, table: str) -> None:
        """Abstract function to write a DataFrame.

        Args:
            df (DataFrame): DataFrame
            table (str): name of the table
        """
        e = "Function 'def custom_write(self, df: DataFrame, table: str) -> None:' needs to be implemented if write(mode=custom)"
        raise NotImplementedError(e)
