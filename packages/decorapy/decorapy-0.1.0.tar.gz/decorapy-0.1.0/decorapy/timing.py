import asyncio
import time
from functools import wraps
from typing import Any, Callable, Optional, Union


def timer(
    format: Optional[str] = "seconds",
    *,
    log_level: Optional[int] = None,
    return_time: bool = False,
    precision: int = 4,
) -> Callable:
    """
    A decorator to measure the time a function takes to execute.

    Args:
        format (Optional[str]): The format to display the elapsed time.
                                - "seconds": Display time in seconds (default).
                                - "hms": Display time in hours, minutes, and seconds.
                                If None, no output is generated.
        log_level (Optional[int]): The logging level for the output message.
                                    If provided, uses Python's logging module instead of print.
                                    Default is None (uses print).
        return_time (bool): Whether to return the elapsed time along with the function's result.
                            Default is False.
        precision (int): Number of decimal places for the elapsed time in seconds.
                            Default is 4.

    Returns:
        Callable: The timed function.

    Example:
        # Basic usage
        @timer(format="seconds")
        def compute():
            time.sleep(1)

        compute()
        # Output: Function compute took 1.0000 seconds to execute

        # Custom logging
        import logging
        logging.basicConfig(level=logging.INFO)

        @timer(format="hms", log_level=logging.INFO)
        def long_task():
            time.sleep(3723)  # 1 hour, 2 minutes, and 3 seconds

        long_task()
        # Logs: INFO - Function long_task took 1h 2m 3.00s to execute

        # Return elapsed time
        @timer(return_time=True)
        def add(a: int, b: int) -> int:
            return a + b

        result, elapsed = add(3, 4)
        print(result, elapsed)  # Output: 7 0.0001
    """
    if format not in (None, "seconds", "hms"):
        raise ValueError("format must be 'seconds', 'hms', or None")

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time

            # Format the elapsed time
            if format == "hms":
                hours, rem = divmod(elapsed_time, 3600)
                minutes, seconds = divmod(rem, 60)
                time_str = f"{int(hours)}h {int(minutes)}m {seconds:.{precision}f}s"
            else:
                time_str = f"{elapsed_time:.{precision}f} seconds"

            # Output the result
            if log_level is not None:
                import logging

                logging.log(
                    log_level, f"Function {func.__name__} took {time_str} to execute"
                )
            elif format is not None:
                print(f"Function {func.__name__} took {time_str} to execute")

            # Return the result and optionally the elapsed time
            if return_time:
                return result, elapsed_time
            return result

        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()
            result = await func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time

            # Format the elapsed time
            if format == "hms":
                hours, rem = divmod(elapsed_time, 3600)
                minutes, seconds = divmod(rem, 60)
                time_str = f"{int(hours)}h {int(minutes)}m {seconds:.{precision}f}s"
            else:
                time_str = f"{elapsed_time:.{precision}f} seconds"

            # Output the result
            if log_level is not None:
                import logging

                logging.log(
                    log_level, f"Function {func.__name__} took {time_str} to execute"
                )
            elif format is not None:
                print(f"Function {func.__name__} took {time_str} to execute")

            # Return the result and optionally the elapsed time
            if return_time:
                return result, elapsed_time
            return result

        return async_wrapper if asyncio.iscoroutinefunction(func) else wrapper

    return decorator
