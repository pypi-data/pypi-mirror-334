import time
from functools import lru_cache, wraps
from typing import Any, Callable, Optional


def lru_memoize(
    maxsize: int = 128,
    *,
    typed: bool = False,
    clearable: bool = False,
    ttl: Optional[float] = None,
) -> Callable:
    """
    A utility to apply LRU (Least Recently Used) memoization to a function.

    Args:
        maxsize (int): Maximum size of the cache. If set to None, the cache can grow indefinitely.
                        Default is 128.
        typed (bool): Whether to differentiate between arguments of different types.
                        For example, 3 and 3.0 would be treated as distinct if True.
                        Default is False.
        clearable (bool): Whether to enable clearing the cache programmatically.
                            If True, the cached function will have a `clear_cache` method
                            to invalidate all cached results.
                            Default is False.
        ttl (Optional[float]): Time-to-live (TTL) for cached results in seconds.
                                If specified, cached results will expire after this duration.
                                Default is None (no expiration).

    Returns:
        Callable: The memoized function.

    Example:
        @lru_memoize(maxsize=32, clearable=True)
        def expensive_computation(x: int) -> int:
            return x ** 2

        # Clear cache if clearable=True
        expensive_computation.clear_cache()

        # Retrieve cache statistics if available
        print(expensive_computation.cache_info())
    """
    if maxsize is not None and maxsize <= 0:
        raise ValueError("maxsize must be a positive integer or None")

    def wrapper(func: Callable) -> Callable:
        # Apply the LRU cache to the function
        cached_func = lru_cache(maxsize=maxsize, typed=typed)(func)

        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> Any:
            # Check TTL for expiration
            if ttl is not None and hasattr(inner, "_last_access"):
                elapsed = time.time() - inner._last_access
                if elapsed > ttl:
                    inner.clear_cache()
            result = cached_func(*args, **kwargs)

            # Update last access time for TTL
            if ttl is not None:
                inner._last_access = time.time()

            return result

        # Add a method to clear the cache if requested
        if clearable:

            def clear_cache() -> None:
                """Clears the cache of the memoized function."""
                cached_func.cache_clear()

            inner.clear_cache = clear_cache  # Attach the method to the wrapper

        # Add a method to retrieve cache statistics
        def cache_info() -> str:
            """Retrieves cache statistics such as hits, misses, and current size."""
            return cached_func.cache_info()

        inner.cache_info = cache_info  # Attach the method to the wrapper

        return inner

    return wrapper
