import daft


def assert_col_in_dataframe(df: daft.DataFrame, col: str) -> None:
    """Function to assert that a column exists in a DataFrame.

    Args:
        df (daft.DataFrame): DataFrame
        col (str): column name
    """

    e = f"Column {col} does not exist in the DataFrame"
    assert col in df.column_names, e
