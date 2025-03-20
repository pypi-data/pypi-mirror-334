import asyncio
import logging
from functools import wraps
from typing import Any, Callable, Optional


def trace(
    func: Optional[Callable] = None,
    *,
    logger: Optional[logging.Logger] = None,
    log_level: int = logging.DEBUG,
    enabled: bool = True,
) -> Callable:
    """
    A decorator to trace function calls and return values for debugging.

    Args:
        func (Optional[Callable]): The function to be traced. If None, this is a decorator factory.
        logger (Optional[logging.Logger]): A custom logger instance to use for tracing.
                                            Default is the root logger.
        log_level (int): The logging level for the trace messages (e.g., logging.DEBUG, logging.INFO).
                            Default is logging.DEBUG.
        enabled (bool): Whether tracing is enabled. If False, the function runs without tracing.
                        Default is True.

    Returns:
        Callable: The traced function.

    Example:
        # Basic usage
        @trace
        def greet(name: str) -> str:
            return f"Hello, {name}!"

        greet("Alice")
        # Logs:
        # DEBUG - TRACE: Calling greet with args: ('Alice',), kwargs: {}
        # DEBUG - TRACE: greet returned Hello, Alice!

        # Custom logger and logging level
        custom_logger = logging.getLogger("custom_logger")
        custom_logger.setLevel(logging.INFO)

        @trace(logger=custom_logger, log_level=logging.INFO)
        def add(a: int, b: int) -> int:
            return a + b

        add(3, 4)
        # Logs:
        # INFO - TRACE: Calling add with args: (3, 4), kwargs: {}
        # INFO - TRACE: add returned 7
    """

    def decorator(func: Callable) -> Callable:
        _logger = (
            logger or logging.getLogger()
        )  # Use the provided logger or the root logger

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if not enabled:
                return func(*args, **kwargs)

            _logger.log(
                log_level,
                f"TRACE: Calling {func.__name__} with args: {args}, kwargs: {kwargs}",
            )
            try:
                result = func(*args, **kwargs)
                _logger.log(log_level, f"TRACE: {func.__name__} returned {result}")
                return result
            except Exception as e:
                _logger.error(f"TRACE: {func.__name__} raised an exception: {e}")
                raise  # Re-raise the exception after logging

        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            if not enabled:
                return await func(*args, **kwargs)

            _logger.log(
                log_level,
                f"TRACE: Calling {func.__name__} with args: {args}, kwargs: {kwargs}",
            )
            try:
                result = await func(*args, **kwargs)
                _logger.log(log_level, f"TRACE: {func.__name__} returned {result}")
                return result
            except Exception as e:
                _logger.error(f"TRACE: {func.__name__} raised an exception: {e}")
                raise  # Re-raise the exception after logging

        return async_wrapper if asyncio.iscoroutinefunction(func) else wrapper

    return decorator if func is None else decorator(func)
