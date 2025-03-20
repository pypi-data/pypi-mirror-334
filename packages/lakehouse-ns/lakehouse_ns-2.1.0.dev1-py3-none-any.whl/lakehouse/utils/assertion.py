from typing import Any, Dict, List


def assert_allowed_opts(options: Dict[str, Any], allowed_opts: List[str]) -> None:
    """Function to assert that only allowed options are provided.
    If options are not in the allowed_opts list an AssertionError is raised.

    Args:
        options (Dict[str, Any]): options provided
        allowed_opts (List[str]): allowed options
    """
    for key in options:
        e = f"Invalid option: {key}, only {allowed_opts} allowed"
        assert key in allowed_opts, e


def assert_required_opts(options: Dict[str, Any], required_opts: List[str]) -> None:
    """Function to assert that all required options are provided.
    If a required option is missing in options an AssertionError is raised.

    Args:
        options (Dict[str, Any]): options provided
        required_opts (List[str]): required options
    """

    for key in required_opts:
        e = f"Missing required option: {key}, required options are {required_opts}"
        assert key in options, e


def assert_load_options(load_opts: Dict[str, Any]) -> None:
    """Function to assert that the load options are valid.

    Args:
        load_opts (Dict[str, Any]): load options
    """

    if "mode" in load_opts.keys():
        e = "Invalid mode, only 'default' or 'custom' allowed"
        assert load_opts["mode"] in [
            "default",
            "custom",
        ], e
    if "filter" in load_opts.keys():
        e = "Invalid filter, only 'all' or 'custom' allowed"
        assert load_opts["filter"] in [
            "all",
            "custom",
            "new",
        ], e
    if "filter" in load_opts.keys() and load_opts["filter"] == "new":
        e = "'date_col' needs to be defined if filter is 'new'"
        assert load_opts["date_col"] is not None, e
    if "source_tbl" in load_opts.keys():
        e = "source_tbl must be None or a string"
        assert load_opts["source_tbl"] is None or isinstance(
            load_opts["source_tbl"], str
        ), e


def assert_transform_options(transform_opts: Dict[str, Any], self) -> None:
    """Function to assert that the transform options are valid.

    Args:
        transform_opts (Dict[str, Any]): transform options
    """
    if "ignore_defaults" in transform_opts.keys():
        e = "ignore_defaults must be a boolean"
        assert isinstance(transform_opts["ignore_defaults"], bool), e
    if "transmformation_order" in transform_opts.keys():
        e = "transformation_order must be a list of strings"
        assert isinstance(transform_opts["transmformation_order"], List)
        e = "transformation_order should not be an empty list"
        assert len(transform_opts["transmformation_order"]) > 0, e
    if "tbl_transformations" in transform_opts.keys():
        e = "tbl_transformations must be a dict[str, str]"
        assert isinstance(transform_opts["tbl_transformations"], dict), e
        for func in transform_opts["tbl_transformations"].values():
            e = f"Function {func} does not exist in class"
            assert callable(getattr(self, func, None)), e
    if "rename_columns" in transform_opts.keys():
        e = "rename_columns must be a dict"
        assert isinstance(transform_opts["rename_columns"], dict), e
    if "select_columns" in transform_opts.keys():
        e = "select_columns must be a dict"
        assert isinstance(transform_opts["select_columns"], dict), e
    if "cast_column_types" in transform_opts.keys():
        e = "cast_column_types must be a dict"
        assert isinstance(transform_opts["cast_column_types"], dict), e


def assert_transform_functions(self, funcs: List[str]) -> None:
    """Function to assert that the transform functions are valid.

    Args:
        instance (Callable): instance
        funcs (List[str]): defined functions
    """
    allowed_funcs = [
        func
        for func in dir(self)
        if callable(getattr(self, func)) and not func.startswith("_")
    ]
    allowed_funcs.remove("default_transform")
    allowed_funcs.remove("transform")
    allowed_funcs.append("tbl_transformations")
    for f in funcs:
        e = f"Invalid function {f}, only {allowed_funcs} allowed"
        assert f in allowed_funcs, e

def assert_write_options(write_opts: Dict[str, Any]) -> None:
    """Function to assert that the write options are valid.

    Args:
        write_opts (Dict[str, Any]): write options
    """

    if "mode" in write_opts.keys():
        e = "Invalid mode, only 'overwrite', 'append', 'replace', 'stream', 'merge' or 'custom' allowed"
        assert write_opts["mode"] in [
            "overwrite",
            "append",
            "replace",
            "stream",
            "merge",
            "custom",
        ], e
    if "merge_schema" in write_opts.keys():
        e = "merge_schema must be a boolean"
        assert isinstance(write_opts["merge_schema"], bool), e
    if "overwrite_schema" in write_opts.keys():
        e1 = "overwrite_schema must be a boolean"
        assert isinstance(write_opts["overwrite_schema"], bool), e1
        if write_opts["overwrite_schema"] is True:
            e2 = "overwrite_schema is only allowed in mode overwrite"
            assert write_opts["mode"] == "overwrite", e2


def assert_optimize_options(optimize_opts: Dict[str, Any]) -> None:
    """Function to assert that the optimize options are valid

    Args:
        optimize_opts (Dict[str, Any]): optimize options
    """

    if "optimize" in optimize_opts.keys():
        e = "optimize must be a boolean"
        assert isinstance(optimize_opts["optimize"], bool), e
    if "optimize_full" in optimize_opts.keys():
        e = "optimize full must be a boolean"
        assert isinstance(optimize_opts["optimize_full"], bool), e
        if optimize_opts["optimize_full"] is True:
            e = "Pls set Optimize to True if you activate the optimize full option"
            assert optimize_opts["optimize"] is True, e
    if "vacuum" in optimize_opts.keys():
        e = "vacuum must be a boolean"
        assert isinstance(optimize_opts["vacuum"], bool), e
    if "vacuum_lite" in optimize_opts.keys():
        e = "vacuum lite must be a boolean"
        assert isinstance(optimize_opts["vacuum_lite"], bool), e
        if optimize_opts["vacuum_lite"] is True:
            e = "Pls set Vacuum to True if you activate the vacuum lite option"
            assert optimize_opts["vacuum"] is True, e
    if "analyze" in optimize_opts.keys():
        e = "analyze must be a boolean"
        assert isinstance(optimize_opts["analyze"], bool), e
    if "retention" in optimize_opts.keys():
        if optimize_opts["retention"]:
            e = "retention must be from type integer"
            assert isinstance(optimize_opts["retention"], int), e
    if "excl_cols" in optimize_opts.keys():
        e = "excl_cols is either null or a list of column name strings"
        if optimize_opts["excl_cols"]:
            assert isinstance(optimize_opts["excl_cols"], List), e


def assert_tblproperties(tbl_properties: Dict[str, Any]) -> None:
    """Function to assert that the optimize options are valid

    Args:
        optimize_opts (Dict[str, Any]): optimize options
    """
    if "clusterby" in tbl_properties.keys():
        e = "clusterby is either null or a list of column name strings"
        if tbl_properties["clusterby"]:
            assert isinstance(tbl_properties["clusterby"], List), e
    if "tblproperties" in tbl_properties.keys():
        if tbl_properties["tblproperties"] is not None:
            e = "tblproperties must be a dict[str,str]"
            assert isinstance(tbl_properties["tblproperties"], dict), e
    for p in ["deletion_vectors", "auto_compact", "optimize_write", "change_data_feed", "row_tracking", "type_widening"]:
        if p in tbl_properties.keys():
            e = f"{p} must be a boolean"
            assert isinstance(tbl_properties[p], bool), e

def assert_execute_options(
    load: bool, transform: bool, write: bool, tbl_properties: bool, optimize: bool
) -> None:
    """Function to assert the execute combinations

    Args:
        load (bool): If load option defined
        transform (bool): If transform option defined
        write (bool): If write option defined
        optimize (bool): If optimize option defined
    """
    o = [load, transform, write]
    if (
        o == [False, True, True]
        or o == [False, True, False]
        or o == [False, False, True]
    ):
        e = "Pls specify at least load() before an execute() if using transform/write"
        raise Exception(e)
    if [load, transform, write, tbl_properties, optimize] == [
        False,
        False,
        False,
        False,
        False,
    ]:
        e = "Pls specify options load, transform, write, tblproperties and/or optimize before execute"
        raise Exception(e)
