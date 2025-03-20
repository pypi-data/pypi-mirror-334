from typing import Literal

intro = """
************* WELCOME *************

Welcome to the Lakehouse-ns Module.
This is a short guideline to make you the start easy.

You can find more details in the docu here: https://nikkthegreek.codeberg.page/
You can find samples here: https://github.com/datanikkthegreek/lakehouse-docu/tree/main/samples
"""

architecture = """
************* Architecture *************

The core architecture of the module is based on the classes ETL, Bronze, Silver and Gold.
 - ETL: This is the generic class you can build your own ETL classes from.
 - Bronze, Silver and Gold: These classes are based on the ETL class and are slightly customized for the common scenarios in each zone.

Besides the class you have different options on class level and during execution of your class
instances grouped by load, transform, write, optimize and tbltproperties.
Further, there are some functions you have or can overwrite depending on your options.

Generally you perform the following steps:
- Import the required class
- Overwrite the required functions
- Create a class instance while defining the class options
- Define your options for load, transform, write, optimize and/or tblproperties (optimize and tblproperties currenlty only for spark)
- Execute the class instance

"""

example_spark = """
************* Example Spark *************

A simple example looks like this:
  from lakehouse import bronze

  spark = <Your Spark Session>

  #Create your schemas
  spark.sql(f"CREATE SCHEMA IF NOT EXISTS <catalog>.<schema>")

  class StarWarsBronze(bronze.Bronze):
    def custom_load(self, table):
        results = []
        query = f"https://swapi.tech/api/{table}"
        json_request = requests.get(query).json()
        results.extend(json_request["results"])

        while json_request["next"]:
              json_request = requests.get(json_request["next"]).json()
              results.extend(json_request["results"])
        return spark.createDataFrame(results)

  bronze_instance = StarWarsBronze(spark, catalog=<catalog>, target_schema=<target_schema>)
  bronze_instance.load().write(mode="overwrite").execute("people", "planets")

See for more details below!
"""

example_daft = """
************* Example Spark *************

A simple example looks like this:
  from lakehouse.daft import bronze, silver, gold
  import daft

  options = {
     "catalog": "<catalog>",
     "target_schema": "<schema>"
  }


  class StarWarsBronze(bronze.Bronze):
     def custom_load(self, table):
        results = []
        query = f"https://swapi.tech/api/{table}"
        json_request = requests.get(query).json()
        results.extend(json_request["results"])

        while json_request["next"]:
              json_request = requests.get(json_request["next"]).json()
              results.extend(json_request["results"])
        return daft.from_pylist(results)

  bronze_instance = StarWarsBronze(spark, **options)
  bronze_instance.load().write(mode="overwrite").execute("people", "planets")

  See for more details below!
"""

class_options = """
************* Class Options *************

Each class requires when initializing the following options:
- spark: The spark session
- catalog: The catalog name
- source_schema: The source schema (except for Bronze)
- target_schema: The target schema

Define the class options as follows:
  class YourClass(Bronze):
    pass

  your_instance = YourClass(spark, catalog=<catalog>, source_schema=<source_schema>, target_schema=<target_schema>)

See also here: https://nikkthegreek.codeberg.page/
"""

load = """
************* Load *************

In Load you can define the following options:
  - mode (str): default or custom, default: default, Mode of loading loads either the table from source_schema.table as default or as defined in the custom_load function. In Bronze always a custom_load function is needed meaning the default is custom
  - filter (str): all, custom or new, default: all, Allows applying directly filters on the loaded data for predicate pushdown using "custom", otherwise "all" data is loaded. New determines based on a datae column which data is new. In Bronze always all data is loaded based on the custom_load function
  - date_col (str): Name of the date column used to determine new data, default: None, must exist in the source and target schema and must be defined if filter is new
  - source_tbl (str): Name of the source table, default: None, If provided the source table is used instead of the provided target table to load data

Options mode, filter and date_col are only available in ETL, Silver and Gold. source_tbl only in ETL and Gold.
See also here: https://nikkthegreek.codeberg.page/

Overwrite also the following functions as required:
  - custom_load(self, table: str) -> DataFrame: Function to customize the way or the source data is loaded. required, if load(mode="custom") else ignored.
  - custom_filter(self, df: DataFrame, table: str) -> DataFrame: Function to filter the loaded dataframe and making use of predicate pushdown. required, if load(filter="custom") else ignored.

Daft includes additionally functions for the source and target_path as catalogs are not supported by default.
  - source_path(self, table: str) -> str: Allows you to specify a dynamic path for the source
  - target_path(self, table: str) -> str: Allows you to specify a dynamic path for the target
    
The module also warns you if your forgot to overwrite a required function.
"""

transform = """
************* Transform *************

In Transform you can define the following options:
  - ignore_defaults (bool): default: False, Ignores executing default transformations as defined in default_transform function if True. Usually used during debugging
  - transformation_order (List[str]): default: ["rename_columns", "tbl_transformations", "select_columns", "cast_column_types"], Allows to define the order of transformations to be executed. Default is
  - tbl_transformations (Dict[str, str]): default: {}, Allows to define custom transformations per table by specifying the table name as key and the function name as value. For the tables it is not defined custom_transform is used.
  - rename_columns (Dict[str, Dict[str, str]]): default: {}, Allows to define column renaming per table by specifying the table name as key and the column renaming as value. The value is a dictionary with the old column name as key and the new column name as value.
  - select_columns (Dict[str, list[str]]): default: {}, Allows to define column selection per table by specifying the table name as key and the column names as value.
  - cast_column_types (Dict[str, Dict[str, str]]): default: {}, Allows to define column casting per table by specifying the table name as key and the column casting as value. The value is a dictionary with the column name as key and the cast type as value.

See also here: https://nikkthegreek.codeberg.page/

Overwrite also the following functions as required:
  - custom_transform(self, df: DataFrame, table: str) -> DataFrame: Function to be optionally overwritten to add custom transformations, only executed if transform() is defined
  - rename_columns(self, df: DataFrame, table: str) -> DataFrame:
  - select_columns(self, df: DataFrame, table: str) -> DataFrame:
  - cast_column_types(self, df: DataFrame, table: str) -> DataFrame: Function to cast column types based on defined config. Can be overwritten.
  - default_transform(self, df: DataFrame, table: str) -> DataFrame: Can be overwritten to add default transformations executed after the the custom transformations. Defaults create a timestamp column with the current timestamp of transformations. Only executed if transform(ignore_defaults=False)

The module also warns you if your forgot to overwrite a required function.
"""

write_spark = """
************* Write *************

In Write you can define the following options:
  - mode (str): overwrite, append, replace, merge or custom, default: append, Defines the mode of writing the data as overwrite, append, replace (define replace filter with function get_replace_condition(), merge (define merge builder with function get_delta_merge_builder(), stream (requires checkpoint_path() function), custom (define custom_write() function)
  - merge_schema (bool): default: False, If the schema should be automatically envolved/merged
  - external (bool): default: False, if True tables are saved as external tables based on the defined path in the path function

See also here: https://nikkthegreek.codeberg.page/

Overwrite also the following functions as required:
  - get_replace_condition(self, df: DataFrame, table: str) -> str: Allows you to define the filter used for the replace where overwrite operation. required if write(mode="replace").
  - get_delta_merge_builder(self, df: DataFrame, delta_table: DeltaTable) -> DeltaMergeBuilder: Allows you to define the merge builder for the merge write into delta. required if write(mode="merge")
  - custom_write(self, df: DataFrame, table: str) -> None: Allows to define a custom write operation. required if write(mode="custom")
  - target_path(self, table: str) -> str: Allows you to specify a dynamic path if using external tables
  - checkpoint_path(self, table: str) -> str: Function to be overwritten to create the checkpoint path if performing a streaming write

The module also warns you if your forgot to overwrite a required function.
"""

write_daft = """
************* Write *************

In Write you can define the following options:
  - mode (str): overwrite, append, replace, merge or custom, default: append, Defines the mode of writing the data as overwrite, append, replace (define replace filter with function get_replace_condition(), merge (define merge builder with function get_delta_merge_builder(), custom (define custom_write() function)
  - overwrite_schema (bool): True if schema should be overwritten, default: False, only available for mode overwrite

See also here: https://nikkthegreek.codeberg.page/

Overwrite also the following functions as required:
  - get_replace_condition(self, df: daft.DataFrame, table: str) -> str: Allows you to define the filter used for the replace where overwrite operation. required if write(mode="replace").
  - get_delta_merge_builder(self, df: daft.DataFrame, delta_table: DeltaTable) -> DeltaMergeBuilder: Allows you to define the merge builder for the merge write into delta. required if write(mode="merge")
  - custom_write(self, df: daft.DataFrame, table: str) -> None: Allows to define a custom write operation. required if write(mode="custom")
  - target_path(self, table: str) -> str: Allows you to specify a dynamic path for the target

The module also warns you if your forgot to overwrite a required function.
"""

tbltproperties = """
************* TBLPROPERTIES *************

In Tblproperties you can define the following options:
  - clusterby (list[str] | None): list of cols to be liquid clustered
  - deletion_vectors (bool): enable deletion vectors (delta.enableDeletionVectors), default True, see also here: https://docs.delta.io/latest/delta-deletion-vectors.html
  - auto_compact (bool): enable auto optimize (delta.autoOptimize.autoCompact), default True: https://docs.delta.io/latest/optimizations-oss.html#auto-compaction
  - optimize_write (bool): enable optimize write (delta.autoOptimize.optimizeWrite), default True, see also here: https://docs.delta.io/latest/optimizations-oss.html#optimized-write
  - change_data_feed (bool): enable change data feed, default True (delta.enableChangeDataFeed): https://docs.delta.io/latest/delta-change-data-feed.html
  - row_tracking (bool): enable row tracking (delta.enableRowTracking), default True: https://docs.delta.io/latest/delta-row-tracking.html
  - type_widening (bool): enable type widening (delta.enableTypeWidening), default False: https://docs.delta.io/latest/delta-type-widening.html
  - tblproperties (Dict[str, str] | None): dict of any delta tblproperties as to https://docs.delta.io/

See also here: https://nikkthegreek.codeberg.page/
"""

optimize = """
************* Optimize *************

In Tblproperties you can define the following options:
  - optimize (bool): execute the optimize command on the given tables
  - optimize_full (bool): execute the optimize as Full mode (needs Liquid clustering)
  - vacuum (bool): execute the vacuum command on the given tables as to the defined retention
  - vacuum_lite (bool): execute the vacuum with lite command
  - analyze (bool): execute the analyze command on the given table to compute statistics
  - retention (int): retention time for files to be considered for vacuum. Retention time must be at higher or equal default retention threshold. The default is 7 days (168 hours). If no value is provided retention threshold is taken. The threshold can be changed with the delta property delta.deletedFileRetentionDuration
  - excl_cols (list[str]): list of cols to be excluded to compute statistics

See also here: https://nikkthegreek.codeberg.page/
"""

def _help(engine: Literal["spark", "daft"] = "spark") -> str:
    """Prints the help message for the given engine.

    Args:
        engine (Literal["spark", "daft"], optional): The engine to print the help message for. Defaults to "spark"."
    
    Returns:
        str: The help message for the given engine.
    """
    if engine == "spark":
        spark_help = "\n".join(
          [
              intro,
              architecture,
              example_spark,
              class_options,
              load,
              transform,
              write_spark,
              tbltproperties,
              optimize,
          ]
        )
        return spark_help
    
    elif engine == "daft":
        daft_help = "\n".join(
          [
              intro,
              architecture,
              example_spark,
              class_options,
              load,
              transform,
              write_spark,
              tbltproperties,
              optimize,
          ]
        )
        return daft_help
