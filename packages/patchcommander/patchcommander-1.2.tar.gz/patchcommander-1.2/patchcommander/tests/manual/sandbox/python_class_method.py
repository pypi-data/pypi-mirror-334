"""
Test file for PatchCommander containing various Python class methods.
Used for testing method-related operations.
"""
import time
import functools
from typing import Dict, List, Optional, Any, Union, Tuple, Callable, TypeVar, Generic

T = TypeVar('T')

def method_decorator(func):
    """Example decorator for methods."""
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        print(f"Calling {func.__name__}")
        start = time.time()
        result = func(self, *args, **kwargs)
        end = time.time()
        print(f"Finished {func.__name__} in {end - start:.2f}s")
        return result
    return wrapper

class MethodTestClass:
    """Class with various method types for testing."""

    def __init__(self, name: str, value: int = 42):
        self.name = name
        self.value = value
        self._private_value = 100

    def simple_method(self) -> str:
        """Simple instance method - UPDATED."""
        return f"Updated simple method: {self.name} with value {self.value}"

    def method_with_args(self, arg1: str, arg2: int, *args, **kwargs) -> Dict:
        """Method with various argument types."""
        result = {
            "arg1": arg1,
            "arg2": arg2,
            "args": args,
            "kwargs": kwargs,
            "self_name": self.name
        }
        return result

    @method_decorator
    @method_decorator
    def decorated_method(self, input_data: str, transform: bool = False) -> str:
        """Method with custom decorator - UPDATED with transform parameter."""
        result = f"Processed: {input_data} by {self.name}"
        return result.upper() if transform else result

    @classmethod
    @staticmethod
    def class_method(cls, param: str) -> 'MethodTestClass':
        """Class method example."""
        return 2

    @staticmethod
    @staticmethod
    def static_method(x: int, y: int, operation: str = "add") -> int:
        """
        Static method example - UPDATED with operation parameter.

        Args:
        x: First number
        y: Second number
        operation: Operation to perform (add, subtract, multiply, divide)

        Returns:
        Result of the operation
        """
        if operation == "add":
            return x + y
        elif operation == "subtract":
            return x - y
        elif operation == "multiply":
            return x * y
        elif operation == "divide":
            return x // y if y != 0 else 0
        else:
            return x + y  # Default to addition

    @property
    def readonly_property(self) -> int:
        """Read-only property."""
        return self.value * 2

    @property
    def read_write_property(self) -> int:
        """Readable property."""
        return self._private_value

    @read_write_property.setter
    def read_write_property(self, value: int) -> None:
        """Writable property."""
        if value < 0:
            raise ValueError("Value must be positive")
        self._private_value = value

    async def async_method(self, items: List[str], transform: bool = False) -> List[str]:
        """
        Asynchronous method - UPDATED with transform parameter.

        Args:
        items: List of items to process
        transform: Whether to transform the result to uppercase

        Returns:
        Processed items
        """
        result = []
        for item in items:
            processed = await self._process_item(item)
            if transform:
                processed = processed.upper()
            result.append(processed)
        return result

    async def _process_item(self, item: str) -> str:
        """Private async helper method."""
        return f"{item} processed by {self.name}"

    def __str__(self) -> str:
        """String representation magic method."""
        return f"MethodTestClass(name={self.name}, value={self.value})"

    def __repr__(self) -> str:
        """Developer representation magic method."""
        return f"MethodTestClass({self.name!r}, {self.value})"

    def __eq__(self, other) -> bool:
        """Equality comparison magic method."""
        if not isinstance(other, MethodTestClass):
            return False
        return self.name == other.name and self.value == other.value

class GenericMethodClass(Generic[T]):
    """Class with generic type methods."""

    def __init__(self, value: T):
        self.value = value

    def get_value(self) -> T:
        """Return the generic typed value."""
        return self.value

    def set_value(self, new_value: T) -> None:
        """Set the generic typed value."""
        self.value = new_value

    def transform(self, transformer: Callable[[T], Union[T, Any]]) -> Any:
        """Apply a transformation to the value."""
        return transformer(self.value)

class OverloadedMethods:
    """Class demonstrating method overloading patterns."""

    def process(self, input_data: Union[str, int, List]) -> Any:
        """Process different input types."""
        if isinstance(input_data, str):
            return self._process_string(input_data)
        elif isinstance(input_data, int):
            return self._process_integer(input_data)
        elif isinstance(input_data, list):
            return self._process_list(input_data)
        else:
            raise TypeError(f"Unsupported input type: {type(input_data)}")

    def _process_string(self, data: str) -> str:
        return f"String processed: {data.upper()}"

    def _process_integer(self, data: int) -> int:
        return data * 2

    def _process_list(self, data: List) -> List:
        return [item for item in data if item]