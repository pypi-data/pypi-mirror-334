import logging
from typing import Any, Callable
import functools
import datetime as dt


def createLogger() -> logging.Logger:
    """Creates a logger object and prints the logging at each step.

    Args:
        name: Name of the logger. In many cases it is the datasource name.

    Returns:
        Logger instance
    """
    formatter = logging.Formatter(
        "%(asctime)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger("Lakehouse")
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger


LOGGER = createLogger()


def log(description: str, tbl_pos: int) -> Callable:
    """
    A decorator for logging the execution of a function.

    Args:
        description: Description of the function execution to log.
        tbl_pos: Position of the table name argument in the function signature.

    Returns:
        Callable - A wrapper function with logging functionality.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            table = args[tbl_pos]
            LOGGER.info(f"{table} | {description} | Started")
            start_time = dt.datetime.now()
            result = func(*args, **kwargs)
            end_time = dt.datetime.now()
            run_time = round((end_time - start_time).seconds / 60, 2)
            LOGGER.info(f"{table} | {description} | Completed in {run_time} min")
            return result

        return wrapper

    return decorator
