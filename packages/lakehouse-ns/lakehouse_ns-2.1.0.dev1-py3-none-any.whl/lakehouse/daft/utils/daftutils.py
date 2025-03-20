import daft
import pandas as pd


def idrange(end: int) -> daft.DataFrame:
    """Returns a DataFrame with an id column from 0 to end-1.

    Args:
        end (int): End of the range.

    Returns:
        DataFrame: DataFrame with an id column from 0 to end-1.
    """
    data = {"id": [i for i in range(end)]}
    daft.from_pylist
    return daft.from_pydict(data)


def assert_frame_equal(
    df1: daft.DataFrame, df2: daft.DataFrame, assert_schema: bool = True
) -> None:
    """Assert that two DataFrames are equal.

    Args:
        df1 (daft.DataFrame): First DataFrame to compare.
        df2 (daft.DataFrame): Second DataFrame to compare.
        assert_schema (bool): If True, assert that the schemas of the two DataFrames are equal. Defaults to True.
    """
    if assert_schema:
        assert_schema_equal(df1.schema(), df2.schema())
    pdf1 = df1.to_pandas()
    pdf2 = df2.to_pandas()
    df1.schema()
    pd.testing.assert_frame_equal(pdf1, pdf2, check_like=True, check_dtype=False)
    """
    a1 = df1.to_arrow()
    a2 = df2.to_arrow()
    assert a1.equal(a2, check_metadata=assert_schema) == True
    """


def assert_schema_equal(schema1: daft.Schema, schema2: daft.Schema) -> None:
    """Assert that two schemas are equal.

    Args:
        schema1 (Schema): First schema to compare.
        schema2 (Schema): Second schema to compare.
    """
    assert schema1.column_names() == schema2.column_names(), "Column names do not match"
    for col in schema1.column_names():
        assert (
            schema1[col].dtype == schema2[col].dtype
        ), f"Data type for column {col} does not match"


def get_daft_dtype(dtype_str: str) -> daft.DataType:
    """Returns the Daft data type corresponding to the given data type string.

    Accepts the Delta and Daft name for the data type. Only primitive types are supported.

    Args:
        dtype_str (str): The data type string.

    Returns:
        DataType: The Daft data type.

    Raises:
        Exception: If the data type is not supported.

    Reference:
        https://www.getdaft.io/projects/docs/en/stable/integrations/delta_lake/#type-system
    """
    dtype_map = {
        "boolean": daft.DataType.bool(),
        "bool": daft.DataType.bool(),
        "byte": daft.DataType.int8(),
        "int8": daft.DataType.int8(),
        "short": daft.DataType.int16(),
        "int16": daft.DataType.int16(),
        "int": daft.DataType.int32(),
        "int32": daft.DataType.int32(),
        "long": daft.DataType.int64(),
        "int64": daft.DataType.int64(),
        "float": daft.DataType.float32(),
        "float32": daft.DataType.float32(),
        "double": daft.DataType.float64(),
        "float64": daft.DataType.float64(),
        "date": daft.DataType.date(),
        "timestamp": daft.DataType.timestamp(timeunit="us", timezone=None),
        "timestampz": daft.DataType.timestamp(timeunit="us", timezone="UTC"),
        "string": daft.DataType.string(),
        "binary": daft.DataType.binary(),
    }
    if dtype_str in dtype_map:
        return dtype_map[dtype_str]
    elif dtype_str.startswith("decimal("):
        return get_decimal_dtype(dtype_str)
    else:
        raise Exception(
            f"{dtype_str} is not a valid Daft data type. Only the following data types are supported: {list(dtype_map.keys())} or decimal(precision, scale)"
        )


def get_decimal_dtype(decimal_str: str) -> daft.DataType:
    """Returns the Daft data type for decimals datatype strings

    Args:
        decimal_str (str): The decimal data type string.

    Returns:
        DataType: The decimal Daft data type
    """
    precision = decimal_str.split("(")[1].split(",")[0]
    scale = decimal_str.split("(")[1].split(",")[1].split(")")[0]
    return daft.DataType.decimal128(int(precision), int(scale))
