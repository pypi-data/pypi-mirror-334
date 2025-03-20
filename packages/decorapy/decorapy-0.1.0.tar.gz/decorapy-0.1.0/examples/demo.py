"""
Demo script to showcase the usage of various decorators from the `pydeco` package.
"""

import asyncio
import logging
import time

# Import necessary modules and decorators
from decorapy.benchmark import benchmark
from decorapy.circuit_breaker import CircuitBreaker
from decorapy.log_calls import log_calls
from decorapy.lru_memoize import lru_memoize
from decorapy.memoization import memoize
from decorapy.retry import retry
from decorapy.singleton import singleton
from decorapy.throttle import throttle
from decorapy.timing import timer
from decorapy.trace import trace
from decorapy.validation import validate

# Configure basic logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# Example 1: Benchmark Decorator
@benchmark
def compute_square(x: int) -> int:
    """Computes the square of a number."""
    return x**2


print("\nExample 1: Benchmark Decorator")
compute_square(5)

# Example 2: Circuit Breaker Decorator
breaker = CircuitBreaker(max_failures=2, reset_timeout=5)


@breaker
def unreliable_function() -> str:
    """Simulates an unreliable function that fails twice before succeeding."""
    if breaker.failure_count < 2:
        raise ConnectionError("Simulated failure")
    return "Success"


print("\nExample 2: Circuit Breaker Decorator")
try:
    print(unreliable_function())
except Exception as e:
    print(e)
time.sleep(6)  # Wait for circuit to reset
print(unreliable_function())


# Example 3: Log Calls Decorator
@log_calls(log_args=True, log_return=True)
def greet(name: str) -> str:
    """Greets a person by name."""
    return f"Hello, {name}!"


print("\nExample 3: Log Calls Decorator")
greet("Alice")


# Example 4: LRU Memoize Decorator
@lru_memoize(maxsize=32, clearable=True)
def expensive_computation(x: int) -> int:
    """Simulates an expensive computation."""
    time.sleep(1)  # Simulate delay
    return x**2


print("\nExample 4: LRU Memoize Decorator")
print(expensive_computation(5))  # First call (cached)
print(expensive_computation(5))  # Second call (retrieved from cache)
expensive_computation.clear_cache()  # Clear cache
print(expensive_computation(5))  # Third call (recalculated)


# Example 5: Memoization Decorator
@memoize(clearable=True)
def fibonacci(n: int) -> int:
    """Calculates the nth Fibonacci number recursively."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


print("\nExample 5: Memoization Decorator")
print(fibonacci(10))  # Calculates and caches results
fibonacci.clear_cache()
print(fibonacci(10))  # Recalculates after clearing cache


# Example 6: Retry Decorator
@retry(retries=3, delay=1, exceptions=ValueError)
def unstable_function() -> str:
    """Simulates a function that may fail intermittently."""
    if unstable_function.attempt < 2:
        raise ValueError("Simulated failure")
    return "Success"


print("\nExample 6: Retry Decorator")
print(unstable_function())


# Example 7: Singleton Decorator
@singleton
class DatabaseConnection:
    """Simulates a database connection as a singleton."""

    def __init__(self):
        print("Initializing database connection")


print("\nExample 7: Singleton Decorator")
db1 = DatabaseConnection()
db2 = DatabaseConnection()
assert db1 is db2  # Both references point to the same instance
DatabaseConnection.clear_instance()
db3 = DatabaseConnection()  # Creates a new instance


# Example 8: Throttle Decorator
@throttle(allowed_per_second=1, enabled=True)
def say_hello(name: str) -> None:
    """Prints a greeting message."""
    print(f"Hello, {name}!")


print("\nExample 8: Throttle Decorator")
say_hello("Alice")  # Executes immediately
say_hello("Bob")  # Waits 1 second before executing


# Example 9: Timer Decorator
@timer(format="seconds", log_level=logging.INFO)
def long_task() -> None:
    """Simulates a long-running task."""
    time.sleep(2)


print("\nExample 9: Timer Decorator")
long_task()


# Example 10: Trace Decorator
@trace(enabled=True, log_level=logging.DEBUG)
def add(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b


print("\nExample 10: Trace Decorator")
add(3, 4)


# Example 11: Validation Decorator
@validate(lambda x: x > 0, lambda y: isinstance(y, str), exception_type=ValueError)
def greet_person(age: int, name: str) -> str:
    """Greets a person with their age and name."""
    return f"Hello, {name}! You are {age} years old."


print("\nExample 11: Validation Decorator")
print(greet_person(25, "Alice"))  # Valid input
try:
    print(greet_person(-5, "Bob"))  # Invalid input
except ValueError as e:
    print(e)


# Example 12: Async Support (Benchmark and Retry)
@benchmark(return_time=True)
async def async_compute_square(x: int) -> tuple[int, float]:
    """Asynchronously computes the square of a number."""
    await asyncio.sleep(1)
    return x**2


@retry(retries=2, delay=1, exceptions=RuntimeError)
async def async_unstable_function() -> str:
    """Simulates an asynchronous function that may fail intermittently."""
    raise RuntimeError("Async failure")


print("\nExample 12: Async Support")


async def main():
    result, elapsed = await async_compute_square(5)
    print(f"Result: {result}, Elapsed Time: {elapsed}")
    try:
        await async_unstable_function()
    except Exception as e:
        print(e)


asyncio.run(main())
