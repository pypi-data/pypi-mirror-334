import os
import sys
import platform
from pyspark.sql import SparkSession


def get_databricks_connect_session() -> SparkSession:
    """Creates a Databricks Connect Spark Session.

        Requires DATABRICKS_HOST, DATABRICKS_TOKEN and DATABRICKS_CLUSTER_ID as env variables.

    Returns:
        Databricks Connect Spark Session
    """
    from databricks.connect import DatabricksSession

    return DatabricksSession.builder.remote(
        host=os.getenv("DATABRICKS_HOST"),
        token=os.getenv("DATABRICKS_TOKEN"),
        cluster_id=os.getenv("DATABRICKS_CLUSTER_ID"),
    ).getOrCreate()


def get_spark_opensource_session() -> SparkSession:
    """Creates a Spark Open Source session.

    Returns:
        Spark Open Source Session


    """
    from delta import configure_spark_with_delta_pip

    if platform.system() == "Windows":
        os.environ["PYSPARK_PYTHON"] = sys.executable
        os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
        print("Adding Python ENV variables on Windows")

    builder = (
        SparkSession.builder.master("local[4]")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
    )
    return configure_spark_with_delta_pip(builder).getOrCreate()
