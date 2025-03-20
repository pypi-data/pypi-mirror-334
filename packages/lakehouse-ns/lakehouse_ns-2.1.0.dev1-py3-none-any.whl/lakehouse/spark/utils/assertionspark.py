from typing import Any, Dict
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame


def assert_col_in_dataframe(df: DataFrame, col: str) -> None:
    """Function to assert that a column exists in a DataFrame.

    Args:
        df (DataFrame): DataFrame
        col (str): column name
    """

    e = f"Column {col} does not exist in the DataFrame"
    assert col in df.columns, e


def assert_class_options(class_options: Dict[str, Any], spark: SparkSession) -> None:
    """Function to assert that the class options are valid.

    Args:
        class_options (Dict[str, Any]): class options
        spark (SparkSession): spark session
    """

    if "catalog" in class_options.keys():
        e = "catalog does not exist"
        ctlgs = spark.catalog.listCatalogs(f"{class_options['catalog']}*")
        ctlgs = [c.name for c in ctlgs]
        assert class_options["catalog"] in ctlgs, e
    if "target_schema" in class_options.keys():
        e = "target_schema does not exist"
        assert spark.catalog.databaseExists(class_options["target_schema"]) is True, e
    if "source_schema" in class_options.keys():
        e = "source_schema does not exist"
        assert spark.catalog.databaseExists(class_options["source_schema"]) is True, e


def assert_optimize_options_per_tbl(
    optimize_opts: Dict[str, Any], spark: SparkSession, tbl_name: str
) -> None:
    """Function to assert that the optimize options are valid on table level

    Args:
        optimize_opts (Dict[str, Any]): optimize options
        spark (SparkSession): spark session
        tbl_name (str): tbl name uri as catalog.schema.table
    """

    if "excl_cols" in optimize_opts.keys():
        if optimize_opts["excl_cols"]:
            cols = spark.read.table(tbl_name).columns
            for ec in optimize_opts["excl_cols"]:
                e = f"Column {ec} does not exist in the table {tbl_name}"
                assert ec in cols, e
