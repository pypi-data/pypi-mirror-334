import asyncio
import logging
from functools import wraps
from typing import Any, Callable, Optional

# Set up basic logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def log_calls(
    func: Optional[Callable] = None,
    *,
    logger: Optional[logging.Logger] = None,
    log_level: int = logging.INFO,
    log_args: bool = True,
    log_return: bool = True,
) -> Callable:
    """
    A utility to log function calls and return values.

    Args:
        func (Optional[Callable]): The function to be logged. If None, this is a decorator factory.
        logger (Optional[logging.Logger]): A custom logger instance to use for logging.
                                            Default is the root logger.
        log_level (int): The logging level for the messages (e.g., logging.DEBUG, logging.INFO).
                            Default is logging.INFO.
        log_args (bool): Whether to log the function arguments (args and kwargs).
                            Default is True.
        log_return (bool): Whether to log the function's return value.
                            Default is True.

    Returns:
        Callable: The logged function.

    Example:
        # Basic usage
        @log_calls
        def greet(name: str) -> str:
            return f"Hello, {name}!"

        greet("Alice")
        # Logs:
        # INFO - Calling greet with args: ('Alice',), kwargs: {}
        # INFO - greet returned Hello, Alice!

        # Custom logger and logging level
        custom_logger = logging.getLogger("custom_logger")
        custom_logger.setLevel(logging.DEBUG)

        @log_calls(logger=custom_logger, log_level=logging.DEBUG)
        def add(a: int, b: int) -> int:
            return a + b

        add(3, 4)
        # Logs:
        # DEBUG - Calling add with args: (3, 4), kwargs: {}
        # DEBUG - add returned 7
    """

    def decorator(func: Callable) -> Callable:
        _logger = (
            logger or logging.getLogger()
        )  # Use the provided logger or the root logger

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if log_args:
                _logger.log(
                    log_level,
                    f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}",
                )
            else:
                _logger.log(log_level, f"Calling {func.__name__}")

            try:
                result = func(*args, **kwargs)
                if log_return:
                    _logger.log(log_level, f"{func.__name__} returned {result}")
                return result
            except Exception as e:
                _logger.error(f"{func.__name__} raised an exception: {e}")
                raise  # Re-raise the exception after logging

        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            if log_args:
                _logger.log(
                    log_level,
                    f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}",
                )
            else:
                _logger.log(log_level, f"Calling {func.__name__}")

            try:
                result = await func(*args, **kwargs)
                if log_return:
                    _logger.log(log_level, f"{func.__name__} returned {result}")
                return result
            except Exception as e:
                _logger.error(f"{func.__name__} raised an exception: {e}")
                raise  # Re-raise the exception after logging

        return async_wrapper if asyncio.iscoroutinefunction(func) else wrapper

    return decorator if func is None else decorator(func)
