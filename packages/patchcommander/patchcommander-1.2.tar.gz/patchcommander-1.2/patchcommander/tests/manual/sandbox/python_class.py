"""
Test file for PatchCommander containing various Python class structures.
Used for testing class-related operations.
"""
import typing
from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Union, Tuple

class SimpleClass:
    """A simple class with basic attributes and methods - UPDATED."""

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.value = 100  # Changed from 42
        self.description = description  # New attribute

    def get_name(self) -> str:
        return f"{self.name} - {self.description}" if self.description else self.name

    def set_value(self, value: int) -> None:
        """New method to set the value."""
        self.value = value

class ClassWithDecorators:
    """Class demonstrating various decorators - MODIFIED."""

    @classmethod
    def from_string(cls, text: str, priority: int = 0) -> 'ClassWithDecorators':
        """Create instance from string with optional priority."""
        return cls(text, priority)

    @property
    def computed_value(self) -> int:
        """Property getter example - MODIFIED."""
        return len(self.value) * 2 + self.priority

    def __init__(self, value: str, priority: int = 0):
        self.value = value
        self.priority = priority  # New attribute

    @classmethod
    def from_dict(cls, data: dict) -> 'ClassWithDecorators':
        """New class method to create instance from a dictionary."""
        return cls(
        data.get('value', ''),
        data.get('priority', 0)
        )

    @staticmethod
    def helper_method() -> bool:
        """Static utility method."""
        return True

@dataclass
class DataClass:
    """Class using dataclass decorator."""
    name: str
    age: int
    tags: List[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []

class InheritedClass(SimpleClass):
    """Class demonstrating inheritance."""

    def __init__(self, name: str, extra: str):
        super().__init__(name)
        self.extra = extra

    def get_name(self) -> str:
        """Override parent method."""
        return f"{self.name} ({self.extra})"

class ComplexClass:
    """Class with complex structure including nested classes and multiple methods."""

    class NestedClass:
        """Nested class definition."""
        def __init__(self, data: Any):
            self.data = data

        def process(self) -> str:
            return str(self.data)

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._cache = {}
        self._initialized = False

    def initialize(self) -> None:
        """Initialize the instance."""
        if not self._initialized:
            for key, value in self.config.items():
                self._cache[key] = self.NestedClass(value)
            self._initialized = True

    def get_value(self, key: str, default: Any = None) -> Any:
        """Get a value from the configuration."""
        if not self._initialized:
            self.initialize()

        if key not in self._cache:
            return default

        return self._cache[key].process()

    async def async_operation(self, input_data: List[str]) -> Dict[str, str]:
        """Asynchronous operation example."""
        result = {}
        for item in input_data:
            result[item] = await self._process_item(item)
        return result

    async def _process_item(self, item: str) -> str:
        """Internal async helper method."""
        return f"Processed: {item}"

# Abstract class example
from abc import ABC, abstractmethod

class AbstractBase(ABC):
    """Abstract base class example."""

    @abstractmethod
    def execute(self, command: str) -> bool:
        """Execute a command."""
        pass

    @abstractmethod
    def query(self, query_string: str) -> List[Dict]:
        """Execute a query."""
        pass

    def helper(self) -> str:
        """Non-abstract method in abstract class."""
        return "Helper method"

class NewUtilityClass:
    """A new utility class with static methods."""

    @staticmethod
    def format_string(text: str, uppercase: bool = False) -> str:
        """Format a string with optional uppercase conversion."""
        formatted = text.strip()
        return formatted.upper() if uppercase else formatted

    @staticmethod
    def calculate_sum(numbers: list) -> int:
        """Calculate the sum of a list of numbers."""
        return sum(numbers)