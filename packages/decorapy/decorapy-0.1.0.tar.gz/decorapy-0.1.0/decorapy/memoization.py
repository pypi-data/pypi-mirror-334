import asyncio
from functools import wraps
from threading import Lock
from typing import Any, Callable, Dict, Optional, Tuple


def memoize(
    func: Optional[Callable] = None,
    *,
    maxsize: Optional[int] = None,
    clearable: bool = False,
) -> Callable:
    """
    A decorator to cache function results for optimization.

    Args:
        func (Optional[Callable]): The function to be memoized. If None, this is a decorator factory.
        maxsize (Optional[int]): Maximum size of the cache. If set to None, the cache can grow indefinitely.
                                    Default is None.
        clearable (bool): Whether to enable clearing the cache programmatically.
                            If True, the decorated function will have a `clear_cache` method
                            to invalidate all cached results.
                            Default is False.

    Returns:
        Callable: The memoized function.

    Example:
        @memoize
        def expensive_computation(x: int) -> int:
            print(f"Computing {x}...")
            return x ** 2

        print(expensive_computation(5))  # Computes and caches the result
        print(expensive_computation(5))  # Retrieves the result from the cache

        # Clear cache if clearable=True
        @memoize(clearable=True)
        def greet(name: str) -> str:
            return f"Hello, {name}!"

        greet("Alice")
        greet.clear_cache()
    """

    def decorator(func: Callable) -> Callable:
        cache: Dict[Tuple[Tuple[Any, ...], frozenset], Any] = {}
        lock = Lock()  # Ensure thread safety
        hits = 0
        misses = 0

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            nonlocal hits, misses
            try:
                key = (args, frozenset(kwargs.items()))
            except TypeError:
                raise ValueError(
                    "Function arguments must be hashable to use memoization."
                )

            with lock:
                if key in cache:
                    hits += 1
                    return cache[key]

                # If maxsize is set, evict the oldest entry if the cache is full
                if maxsize is not None and len(cache) >= maxsize:
                    cache.pop(next(iter(cache)))

                misses += 1
                result = func(*args, **kwargs)
                cache[key] = result
                return result

        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            nonlocal hits, misses
            try:
                key = (args, frozenset(kwargs.items()))
            except TypeError:
                raise ValueError(
                    "Function arguments must be hashable to use memoization."
                )

            with lock:
                if key in cache:
                    hits += 1
                    return cache[key]

                # If maxsize is set, evict the oldest entry if the cache is full
                if maxsize is not None and len(cache) >= maxsize:
                    cache.pop(next(iter(cache)))

                misses += 1
                result = await func(*args, **kwargs)
                cache[key] = result
                return result

        # Add a method to clear the cache if requested
        if clearable:

            def clear_cache() -> None:
                """Clears the cache of the memoized function."""
                nonlocal hits, misses
                with lock:
                    cache.clear()
                    hits = 0
                    misses = 0

            wrapper.clear_cache = clear_cache  # Attach the method to the wrapper
            if asyncio.iscoroutinefunction(func):
                async_wrapper.clear_cache = (
                    clear_cache  # Attach the method to the async wrapper
                )

        # Add a method to retrieve cache statistics
        def cache_info() -> Dict[str, Any]:
            """Retrieves cache statistics such as hits, misses, and current size."""
            with lock:
                return {
                    "hits": hits,
                    "misses": misses,
                    "current_size": len(cache),
                }

        wrapper.cache_info = cache_info  # Attach the method to the wrapper
        if asyncio.iscoroutinefunction(func):
            async_wrapper.cache_info = (
                cache_info  # Attach the method to the async wrapper
            )

        return async_wrapper if asyncio.iscoroutinefunction(func) else wrapper

    return decorator if func is None else decorator(func)
