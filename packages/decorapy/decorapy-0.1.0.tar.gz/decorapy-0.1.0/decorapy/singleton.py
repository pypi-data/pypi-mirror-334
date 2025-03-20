from functools import wraps
from threading import Lock
from typing import Any, Type


def singleton(cls: Type) -> Type:
    """
    A decorator to ensure a class has only one instance (Singleton pattern).

    Args:
        cls (Type): The class to be decorated.

    Returns:
        Type: The singleton class.

    Example:
        @singleton
        class DatabaseConnection:
            def __init__(self):
                print("Initializing database connection")

        db1 = DatabaseConnection()
        db2 = DatabaseConnection()

        assert db1 is db2  # Both references point to the same instance

        # Clear the singleton instance
        DatabaseConnection.clear_instance()
        db3 = DatabaseConnection()  # Creates a new instance
    """
    instances: dict[Type, Any] = {}
    lock = Lock()  # Ensure thread safety

    @wraps(cls)
    def get_instance(*args: Any, **kwargs: Any) -> Any:
        with lock:
            if cls not in instances:
                # Create the instance only if it doesn't already exist
                instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    # Add a method to clear the singleton instance
    def clear_instance() -> None:
        """Clears the singleton instance, allowing a new instance to be created."""
        with lock:
            if cls in instances:
                del instances[cls]

    # Attach the clear_instance method to the class
    setattr(get_instance, "clear_instance", clear_instance)

    return get_instance
