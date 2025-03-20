import asyncio
import logging
import time
from functools import wraps
from typing import Any, Callable, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)


def benchmark(
    func: Optional[Callable] = None,
    *,
    log_level: int = logging.INFO,
    message_format: str = "{func_name} executed in {elapsed_time:.4f} seconds",
    enabled: bool = True,
    return_time: bool = False,
) -> Callable:
    """
    A decorator to benchmark the execution time of a function.

    Args:
        func (Optional[Callable]): The function to be benchmarked. If None, this is a decorator factory.
        log_level (int): The logging level for the benchmark message (default: logging.INFO).
        message_format (str): Custom format for the benchmark message. Supports placeholders:
                                - {func_name}: Name of the function.
                                - {elapsed_time}: Execution time in seconds.
        enabled (bool): Whether benchmarking is enabled. If False, the function runs without benchmarking.
        return_time (bool): Whether to return the execution time along with the function's result.

    Returns:
        Callable: The benchmarked function.

    Example:
        @benchmark
        def compute():
            time.sleep(1)

        compute()  # Logs: "compute executed in 1.0001 seconds"

        @benchmark(return_time=True)
        def compute_with_time():
            time.sleep(1)

        result, elapsed = compute_with_time()
        print(elapsed)  # Prints: 1.0001
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if not enabled:
                return func(*args, **kwargs)

            start_time = time.perf_counter()
            try:
                result = func(*args, **kwargs)
            finally:
                end_time = time.perf_counter()
                elapsed_time = end_time - start_time
                log_message = message_format.format(
                    func_name=func.__name__,
                    elapsed_time=elapsed_time,
                )
                logger.log(log_level, log_message)

            if return_time:
                return result, elapsed_time
            return result

        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            if not enabled:
                return await func(*args, **kwargs)

            start_time = time.perf_counter()
            try:
                result = await func(*args, **kwargs)
            finally:
                end_time = time.perf_counter()
                elapsed_time = end_time - start_time
                log_message = message_format.format(
                    func_name=func.__name__,
                    elapsed_time=elapsed_time,
                )
                logger.log(log_level, log_message)

            if return_time:
                return result, elapsed_time
            return result

        return async_wrapper if asyncio.iscoroutinefunction(func) else wrapper

    return decorator if func is None else decorator(func)
