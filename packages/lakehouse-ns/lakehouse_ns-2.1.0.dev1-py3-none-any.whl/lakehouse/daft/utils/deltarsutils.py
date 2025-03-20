import deltalake


def delta_table_exists(path):
    """Checks if a Delta table exists at the specified path.

    Args:
        path (str): The path to the Delta table.

    Returns:
        bool: True if the Delta table exists, False otherwise.
    """
    try:
        # Attempt to load the Delta table
        deltalake.DeltaTable(path)
        return True
    except Exception:
        # If an exception is raised, the table likely does not exist
        return False
