from lakehouse.utils import helper
from typing import Literal

def help(engine: Literal["spark", "daft"] = "spark") -> None:
    """Prints the help message for the given engine.

    Args:
        engine (Literal["spark", "daft"], optional): The engine to print the help message for. Defaults to "spark"."
    
    Returns:
        str: The help message for the given engine.
    """
    assert engine in ["spark", "daft"], "Engine must be spark or daft"
    print(helper._help(engine))
