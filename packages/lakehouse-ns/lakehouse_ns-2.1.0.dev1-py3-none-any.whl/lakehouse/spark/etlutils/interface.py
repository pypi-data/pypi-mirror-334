from pyspark.sql import SparkSession
from typing import Any, Dict
from lakehouse.spark.utils import assertionspark


class Interface:
    """A generic class as imterface for etl classes

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
        """Initializes the class with user-provided options.

        Args:
            spark (SparkSession): existing Spark Session
            catalog (str): Name of the created catalog recognized by spark e.g. from Hive Metastore or Unity Catalogue, required
            source_schema (str): Name of the source_schema, required
            target_schema (str): Name of the target_schema, required
            **options (Dict[str, Any]): Kwargs, Any other options provided into the class
        """
        opts = {
            "catalog": catalog,
            "source_schema": source_schema,
            "target_schema": target_schema,
        }
        assertionspark.assert_class_options(opts, spark)
        self.spark = spark
        self.catalog = catalog
        spark.catalog.setCurrentCatalog(catalog)
        self.source_schema = source_schema
        self.target_schema = target_schema
        self.options = options
