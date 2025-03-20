import asyncio
import logging
import time
from functools import wraps
from typing import Any, Callable, Optional, Type, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def retry(
    retries: int = 3,
    delay: float = 1.0,
    exceptions: Union[Type[Exception], tuple] = Exception,
    on_failure: Optional[Any] = None,
    logger: Optional[logging.Logger] = None,
) -> Callable:
    """
    A decorator to retry a function if it raises a specified exception.

    Args:
        retries (int): Number of retries before giving up. Default is 3.
        delay (float): Initial delay between retries in seconds. Default is 1.0.
        exceptions (Union[Type[Exception], tuple]): The exception(s) that should trigger a retry.
                                                    Default is Exception (all exceptions).
        on_failure (Optional[Any]): The value to return if all retries fail.
                                        If None, the last exception is re-raised. Default is None.
        logger (Optional[logging.Logger]): A custom logger instance to use for logging.
                                            Default is the root logger.

    Returns:
        Callable: The decorated function.

    Example:
        # Basic usage
        @retry(retries=3, delay=1)
        def unreliable_function():
            if unreliable_function.attempt < 2:
                raise ValueError("Simulated failure")
            return "Success"

        print(unreliable_function())  # May succeed after retries

        # Custom exceptions and exponential backoff
        @retry(retries=5, delay=0.5, exceptions=(ConnectionError,))
        def fetch_data():
            raise ConnectionError("Failed to connect")

        try:
            fetch_data()
        except Exception as e:
            print(e)  # All retries failed

        # Asynchronous function
        @retry(retries=3, delay=1)
        async def async_unreliable_function():
            await asyncio.sleep(1)
            raise RuntimeError("Async failure")

        asyncio.run(async_unreliable_function())
    """
    if retries < 0:
        raise ValueError("retries must be non-negative")
    if delay < 0:
        raise ValueError("delay must be non-negative")

    _logger = (
        logger or logging.getLogger()
    )  # Use the provided logger or the root logger

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(retries + 1):  # Include the initial attempt
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == retries:
                        _logger.error(
                            f"All {retries} retries failed for {func.__name__}: {e}"
                        )
                        if on_failure is not None:
                            return on_failure
                        raise  # Re-raise the exception if no fallback is provided
                    _logger.warning(
                        f"Attempt {attempt + 1} failed for {func.__name__}: {e}"
                    )
                    time.sleep(delay * (2**attempt))  # Exponential backoff

        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(retries + 1):  # Include the initial attempt
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    if attempt == retries:
                        _logger.error(
                            f"All {retries} retries failed for {func.__name__}: {e}"
                        )
                        if on_failure is not None:
                            return on_failure
                        raise  # Re-raise the exception if no fallback is provided
                    _logger.warning(
                        f"Attempt {attempt + 1} failed for {func.__name__}: {e}"
                    )
                    await asyncio.sleep(delay * (2**attempt))  # Exponential backoff

        return async_wrapper if asyncio.iscoroutinefunction(func) else wrapper

    return decorator
