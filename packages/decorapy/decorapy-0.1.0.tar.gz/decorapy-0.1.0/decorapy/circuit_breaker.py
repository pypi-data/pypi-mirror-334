import asyncio
import threading
import time
from functools import wraps
from typing import Any, Callable, Optional, Type, Union


class CircuitBreaker:
    """
    A Circuit Breaker implementation to prevent cascading failures in distributed systems.

    The circuit breaker monitors the number of consecutive failures in a function call.
    If the number of failures exceeds a specified threshold (`max_failures`), the circuit
    breaker opens and prevents further calls to the function for a specified duration
    (`reset_timeout`). After the timeout expires, the circuit breaker enters a half-open
    state, allowing one trial call to test if the function is working again. If the trial
    succeeds, the circuit closes; otherwise, it remains open.

    Args:
        max_failures (int): Maximum number of consecutive failures before opening the circuit.
                            Must be greater than 0.
        reset_timeout (float): Time in seconds to wait before resetting the circuit.
                                Must be non-negative.
        exception_type (Optional[Type[Exception]]): The type of exception that triggers the circuit breaker.
                                                    Default is Exception (all exceptions).
        name (Optional[str]): A name for the circuit breaker for logging and debugging purposes.
                                Default is None.

    Example:
        ```
        # Define a circuit breaker with a maximum of 3 failures and a reset timeout of 5 seconds
        breaker = CircuitBreaker(max_failures=3, reset_timeout=5)

        @breaker
        def unreliable_function():
            if breaker.failure_count < 2:
                raise ConnectionError("Simulated failure")
            return "Success"

        try:
            print(unreliable_function())  # May raise an exception if the circuit is open
        except Exception as e:
            print(e)

        # Wait for the circuit to reset
        time.sleep(6)
        print(unreliable_function())  # Success
        ```

        ```
        breaker = CircuitBreaker(max_failures=2, reset_timeout=5, exception_type=ValueError)

        @breaker
        def test_function(x: int):
            if x < 0:
                raise ValueError("Invalid value")
            return x

        print(test_function(10))  # Success
        print(test_function(-1))  # Circuit breaker opens after 2 failures
        ```
    """

    def __init__(
        self,
        max_failures: int,
        reset_timeout: float,
        exception_type: Optional[Type[Exception]] = Exception,
        name: Optional[str] = None,
    ) -> None:
        if max_failures <= 0:
            raise ValueError("max_failures must be greater than 0")
        if reset_timeout < 0:
            raise ValueError("reset_timeout must be non-negative")

        self.max_failures = max_failures
        self.reset_timeout = reset_timeout
        self.exception_type = exception_type
        self.name = name or "CircuitBreaker"
        self.failure_count = 0
        self.last_failure_time: Optional[float] = None
        self.lock = threading.Lock()  # Ensure thread safety

    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with self.lock:  # Ensure thread-safe access to shared state
                # Check if the circuit is open
                if self.failure_count >= self.max_failures:
                    if (
                        self.last_failure_time
                        and time.time() - self.last_failure_time < self.reset_timeout
                    ):
                        raise Exception(
                            f"{self.name} is open due to {self.failure_count} failures. "
                            f"Try again after {self.reset_timeout - (time.time() - self.last_failure_time):.2f} seconds."
                        )
                    else:
                        # Reset the circuit breaker after the timeout
                        self.failure_count = 0

            try:
                result = func(*args, **kwargs)
                with self.lock:
                    self.failure_count = 0  # Reset failure count on success
                return result
            except self.exception_type as e:
                with self.lock:
                    self.failure_count += 1
                    self.last_failure_time = time.time()
                raise e

        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            with self.lock:  # Ensure thread-safe access to shared state
                # Check if the circuit is open
                if self.failure_count >= self.max_failures:
                    if (
                        self.last_failure_time
                        and time.time() - self.last_failure_time < self.reset_timeout
                    ):
                        raise Exception(
                            f"{self.name} is open due to {self.failure_count} failures. "
                            f"Try again after {self.reset_timeout - (time.time() - self.last_failure_time):.2f} seconds."
                        )
                    else:
                        # Reset the circuit breaker after the timeout
                        self.failure_count = 0

            try:
                result = await func(*args, **kwargs)
                with self.lock:
                    self.failure_count = 0  # Reset failure count on success
                return result
            except self.exception_type as e:
                with self.lock:
                    self.failure_count += 1
                    self.last_failure_time = time.time()
                raise e

        # Determine whether to use the synchronous or asynchronous wrapper
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return wrapper

    def is_open(self) -> bool:
        """
        Check if the circuit breaker is open.

        Returns:
            bool: True if the circuit breaker is open, False otherwise.
        """
        with self.lock:
            return (
                self.failure_count >= self.max_failures
                and self.last_failure_time
                and time.time() - self.last_failure_time < self.reset_timeout
            )

    def is_closed(self) -> bool:
        """
        Check if the circuit breaker is closed.

        Returns:
            bool: True if the circuit breaker is closed, False otherwise.
        """
        return not self.is_open()

    def reset(self) -> None:
        """
        Manually reset the circuit breaker to its initial state.
        """
        with self.lock:
            self.failure_count = 0
            self.last_failure_time = None
