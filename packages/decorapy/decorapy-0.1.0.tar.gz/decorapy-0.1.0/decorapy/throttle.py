import time
from functools import wraps
from threading import Lock
from typing import Any, Callable


def throttle(*, allowed_per_second: int, enabled: bool = True) -> Callable:
    """
    A decorator to limit the rate at which a function can be called.

    Args:
        allowed_per_second (int): The maximum number of calls allowed per second.
        enabled (bool): Whether rate limiting is enabled. If False, the function runs without rate limiting.

    Returns:
        Callable: The rate-limited function.

    Example:
        @throttle(allowed_per_second=1)
        def say_hello(name: str):
            print(f"Hello, {name}!")

        say_hello("Alice")  # Executes immediately
        say_hello("Bob")    # Waits 1 second before executing
    """
    if allowed_per_second <= 0:
        raise ValueError("allowed_per_second must be greater than 0")

    max_period = 1.0 / allowed_per_second
    last_call = [time.perf_counter()]
    lock = Lock()

    def decorate(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if not enabled:
                return func(*args, **kwargs)

            with lock:
                elapsed = time.perf_counter() - last_call[0]
                hold = max_period - elapsed
                if hold > 0:
                    time.sleep(hold)
                result = func(*args, **kwargs)
                last_call[0] = time.perf_counter()

            return result

        return wrapper

    return decorate
