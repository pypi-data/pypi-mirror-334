"""
LoguruPro: Enhanced Loguru Logger

This module provides an enhanced wrapper for the Loguru logger with additional features.

Usage:
    from pibrary.loguru import logger

The `logger` object is a pre-instantiated LoguruPro instance, ready to use.

Features:
    - Custom log levels: TIME and DATA
    - Execution time measurement
    - Tabular data logging

Example:
    from pibrary.loguru import logger

    # Logging at custom levels
    logger.time("This is a time log")
    logger.data("This is a data log")

    # Using timeit as a decorator
    @logger.timeit
    def my_function():
        # Your code here
        pass

    # Using timeit as a context manager
    with logger.timeit():
        # Your code block here
        pass

    # Logging a table
    data = [
        ["Alice", "25", "Engineer"],
        ["Bob", "30", "Designer"],
        ["Charlie", "35", "Manager"]
    ]
    headers = ["Name", "Age", "Profession"]
    logger.log_table(data, headers=headers)
"""

import inspect
import sys

from time import time

from typing import Any, Callable, Dict, List, Optional, Tuple
from functools import wraps
from loguru import logger as loguru_logger


def format_elapsed_time(seconds: float) -> str:
    """Format elapsed time into hours, minutes, and seconds."""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    parts = []
    if hours > 0:
        parts.append(f"{int(hours)}h")
    if minutes > 0 or hours > 0:
        parts.append(f"{int(minutes)}m")

    if seconds >= 1:
        parts.append(f"{seconds:.2f}s")
    elif seconds >= 0.001:
        parts.append(f"{seconds*1000:.2f}ms")
    else:
        parts.append(f"{seconds*1000000:.2f}µs")

    return " ".join(parts)


class TimerContextManager:
    """
    Context manager to measure and log the execution time of code blocks.

    Attributes:
        logger (loguru_logger): Instance of the Loguru logger for logging.
        start_time (float): The time when the context was entered.
    """

    def __init__(self, logger: loguru_logger) -> None:
        """
        Initializes the TimerContextManager with a Loguru logger.

        Args:
            logger (loguru_logger): The logger instance used for logging execution time.
        """
        self.logger = logger

    def __enter__(self) -> "TimerContextManager":
        """Record the start time when entering the context."""
        self.start_time = time()
        return self

    def __exit__(self, exc_type: Optional[type], exc_val: Optional[BaseException], exc_tb: Optional[Any]) -> None:
        """Log the elapsed time when exiting the context."""
        elapsed_time = time() - self.start_time
        elapsed_time_str = format_elapsed_time(elapsed_time)

        self.logger.opt(depth=1).log("TIME", f"Code block executed in {elapsed_time_str}.")


class LoguruPro:
    """
    Enhanced wrapper for Loguru logger with additional features.

    Note: This class is not intended to be instantiated directly.
    Use the pre-instantiated `logger` object from this module.
    """

    def __init__(self) -> None:
        """Initialize LoguruPro with custom log levels."""
        self.logger = loguru_logger
        self._setup_custom_levels()

    def _setup_custom_levels(self) -> None:
        """Define custom log levels for TIME and DATA."""
        self.logger.level("TIME", no=15, icon="⏱️", color="<bold><magenta>")
        self.logger.level("DATA", no=100, icon="📊", color="<bold><cyan>")

    def __getattr__(self, name: str) -> Callable:
        """
        Delegate attribute access to the wrapped Loguru logger object.

        Args:
            name (str): The attribute or method name to access.

        Returns:
            Callable: The corresponding attribute or method from the Loguru logger.
        """
        return getattr(self.logger, name)

    def time(self, message: str) -> None:
        """
        Log a message at the custom TIME level.

        Args:
            message (str): The message to log.

        Usage:
            logger.time("Operation completed")
        """
        self.logger.opt(depth=1).log("TIME", message)

    def data(self, message: str) -> None:
        """
        Log a message at the custom DATA level.

        Args:
            message (str): The message to log.

        Usage:
            logger.data("Data processing result: 42")
        """
        self.logger.opt(depth=1).log("DATA", message)

    def timeit(self, function: Optional[Callable] = None) -> Callable:
        """
        Decorator or context manager for logging execution time.

        Args:
            function (Optional[Callable]): The function to time if used as a decorator.

        Returns:
            Callable: The wrapped function with timing or a context manager.

        Usage as a decorator:
            @logger.timeit
            def my_function():
                # Your code here
                pass

        Usage as a context manager:
            with logger.timeit():
                # Your code block here
                pass
        """
        if function:

            @wraps(function)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                self.logger.trace(f"Entering {function.__name__}.")
                start_time = time()
                result = function(*args, **kwargs)
                elapsed_time = time() - start_time
                self.logger.opt(depth=1).log("TIME", f"{function.__name__} ran in {format_elapsed_time(elapsed_time)}.")
                self.logger.trace(f"Exiting {function.__name__}.")
                return result

            return wrapper

        return TimerContextManager(self.logger)

    def log_table(
        self,
        data: List[List[str]],
        headers: Optional[List[str]] = None,
        alignments: Optional[List[str]] = None,
        row_separator: str = "-+-",
        column_separator: str = " | ",
    ) -> None:
        """
        Log a list of data as a formatted table.

        Args:
            data (List[List[str]]): The rows of the table, where each row is a list of string values.
            headers (Optional[List[str]]): The headers for the table columns.
            alignments (Optional[List[str]]): Alignment for each column ("left", "center", "right").
            row_separator (str): The string used to separate rows. Default is '-+-'.
            column_separator (str): The string used to separate columns. Default is ' | '.

        Usage:
            data = [
                ["Alice", "25", "Engineer"],
                ["Bob", "30", "Designer"],
                ["Charlie", "35", "Manager"]
            ]
            headers = ["Name", "Age", "Profession"]
            logger.log_table(data, headers=headers)
        """
        num_columns = max(len(row) for row in data)
        headers = headers or [f"Column {i + 1}" for i in range(num_columns)]
        alignments = (alignments or ["left"] * num_columns)[:num_columns]

        # Calculate the maximum width for each column
        col_widths = [max(len(str(item)) for item in col) for col in zip(headers, *data)]

        def format_cell(value: str, width: int, align: str) -> str:
            """Format a cell based on the specified alignment."""
            align_map = {"left": "<", "center": "^", "right": ">"}
            return f"{value:{align_map.get(align, '<')}{width}}"

        def format_row(row: List[str]) -> str:
            """Format a row with the specified column separator."""
            return column_separator.join(format_cell(item, col_widths[i], alignments[i]) for i, item in enumerate(row))

        separator_row = row_separator.join("-" * width for width in col_widths)
        table = "\n".join([format_row(headers), separator_row] + [format_row(row) for row in data])

        self.logger.log("DATA", f"Table of Results:\n{table}")


# Instantiate the logger
logger = LoguruPro()

__all__ = ["logger"]
