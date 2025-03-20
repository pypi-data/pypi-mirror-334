import asyncio
from functools import wraps
from inspect import signature
from typing import Any, Callable, Optional, Type


def validate(
    *validators: Callable[..., bool],
    skip_validation: bool = False,
    return_validator: Optional[Callable[..., bool]] = None,
    exception_type: Type[Exception] = ValueError,
) -> Callable:
    """
    A decorator to validate function arguments and optionally the return value using custom validators.

    Args:
        *validators (Callable[..., bool]): The validation functions for positional arguments.
                                            Validators are applied in the order of positional arguments.
        skip_validation (bool): Whether to skip validation. If True, the function runs without validation.
                                Default is False.
        return_validator (Optional[Callable[..., bool]]): A validator for the return value of the function.
                                                            Default is None (no return value validation).
        exception_type (Type[Exception]): The exception type to raise when validation fails.
                                            Default is ValueError.

    Returns:
        Callable: The decorated function.

    Example:
        # Basic usage
        @validate(lambda x: x > 0, lambda y: isinstance(y, str))
        def greet(age: int, name: str) -> str:
            return f"Hello, {name}! You are {age} years old."

        greet(25, "Alice")  # Valid
        greet(-5, "Bob")    # Raises ValueError: Argument 0 is invalid: -5

        # Validate return value
        @validate(return_validator=lambda result: result.startswith("Hello"))
        def greet(name: str) -> str:
            return f"Hi, {name}!"

        greet("Alice")  # Raises ValueError: Return value is invalid: Hi, Alice!

        # Custom exception type
        @validate(lambda x: x > 0, exception_type=TypeError)
        def compute(x: int) -> int:
            return x ** 2

        compute(-5)  # Raises TypeError: Argument 0 is invalid: -5
    """

    def decorator(func: Callable) -> Callable:
        sig = signature(func)

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if skip_validation:
                return func(*args, **kwargs)

            # Validate positional arguments
            for i, (arg, validator) in enumerate(zip(args, validators)):
                if not validator(arg):
                    raise exception_type(f"Argument {i} is invalid: {arg}")

            # Validate keyword arguments
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            for param_name, param_value in bound_args.arguments.items():
                if param_name in kwargs:
                    validator_idx = list(sig.parameters.keys()).index(param_name)
                    if validator_idx < len(validators) and not validators[
                        validator_idx
                    ](param_value):
                        raise exception_type(
                            f"Argument '{param_name}' is invalid: {param_value}"
                        )

            # Call the function
            result = func(*args, **kwargs)

            # Validate return value
            if return_validator is not None and not return_validator(result):
                raise exception_type(f"Return value is invalid: {result}")

            return result

        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            if skip_validation:
                return await func(*args, **kwargs)

            # Validate positional arguments
            for i, (arg, validator) in enumerate(zip(args, validators)):
                if not validator(arg):
                    raise exception_type(f"Argument {i} is invalid: {arg}")

            # Validate keyword arguments
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            for param_name, param_value in bound_args.arguments.items():
                if param_name in kwargs:
                    validator_idx = list(sig.parameters.keys()).index(param_name)
                    if validator_idx < len(validators) and not validators[
                        validator_idx
                    ](param_value):
                        raise exception_type(
                            f"Argument '{param_name}' is invalid: {param_value}"
                        )

            # Call the function
            result = await func(*args, **kwargs)

            # Validate return value
            if return_validator is not None and not return_validator(result):
                raise exception_type(f"Return value is invalid: {result}")

            return result

        return async_wrapper if asyncio.iscoroutinefunction(func) else wrapper

    return decorator
