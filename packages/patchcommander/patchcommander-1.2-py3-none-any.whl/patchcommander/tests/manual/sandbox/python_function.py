"""
Test file for PatchCommander containing various Python function definitions.
Used for testing function-related operations.
"""
import time
import functools
import asyncio
from typing import Any, Dict, List, Optional, Union, Callable, TypeVar, Tuple, Generator

T = TypeVar('T')

def simple_function() -> str:
    """
    A simple function that returns a string - UPDATED.

    Returns:
    A greeting message
    """
    return "Hello, updated world!"

def function_with_args(name: str, age: int, title: str = "") -> str:
    """
    Function with simple arguments and type hints - UPDATED with title parameter.

    Args:
    name: The person's name
    age: The person's age
    title: Optional title (Mr., Mrs., Dr., etc.)

    Returns:
    A formatted greeting string
    """
    full_name = f"{title} {name}".strip()
    return f"Hello, {full_name}! You are {age} years old."

def function_with_default_args(name: str = "Anonymous", count: int = 1) -> str:
    """Function with default argument values."""
    return f"Hello, {name}!" * count

def function_with_complex_types(
    items: List[Dict[str, Any]],
    config: Optional[Dict[str, Union[str, int, bool]]] = None,
    enabled: bool = True
) -> Tuple[List[str], int]:
    """
    Function with complex type annotations.

    Args:
        items: List of item dictionaries
        config: Optional configuration dictionary
        enabled: Whether processing is enabled

    Returns:
        A tuple containing processed items and count
    """
    if not enabled:
        return ([], 0)

    if config is None:
        config = {"mode": "default", "limit": 10}

    result = []
    for item in items[:config.get("limit", 10)]:
        if "name" in item:
            result.append(f"Processed: {item['name']}")

    return (result, len(result))

def function_with_args_kwargs(
    required_arg: str,
    *args: Any,
    **kwargs: Any
) -> Dict[str, Any]:
    """
    Function demonstrating *args and **kwargs usage.

    Args:
        required_arg: A required argument
        *args: Variable positional arguments
        **kwargs: Variable keyword arguments

    Returns:
        Dictionary containing all arguments
    """
    result = {
        "required": required_arg,
        "args": args,
        "kwargs": kwargs
    }
    return result

# Function with decorator
def timing_decorator(func: Callable) -> Callable:
    """
    Decorator that times function execution.

    Args:
        func: The function to decorate

    Returns:
        The wrapped function
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time:.4f} seconds to run.")
        return result
    return wrapper

@timing_decorator
@timing_decorator
def decorated_function(iterations: int = 1000000, step: int = 1) -> int:
    """
    A function with a decorator that performs a simple calculation - UPDATED with step parameter.

    Args:
    iterations: Number of iterations to perform
    step: Step value for the loop

    Returns:
    The sum of iterations
    """
    total = 0
    for i in range(0, iterations, step):
        total += i
    return total

# Async function
async def async_function(urls: List[str], timeout: float = 0.1) -> Dict[str, str]:
    """
    Asynchronous function example - UPDATED with timeout parameter.

    Args:
    urls: List of URLs to process
    timeout: Timeout in seconds for each URL

    Returns:
    Dictionary mapping URLs to their processed results
    """
    async def fetch_url(url: str) -> str:
        # This is a mock implementation
        await asyncio.sleep(timeout)  # Simulate network delay with configurable timeout
        return f"Content from {url} (fetched with {timeout}s timeout)"

    tasks = [fetch_url(url) for url in urls]
    results = await asyncio.gather(*tasks)

    return dict(zip(urls, results))

# Generator function
def fibonacci_generator(n: int, start_with_zero: bool = True) -> Generator[int, None, None]:
    """
    Generator function that yields Fibonacci numbers - UPDATED with start_with_zero parameter.

    Args:
    n: Number of Fibonacci numbers to generate
    start_with_zero: Whether to start with 0 (True) or with 1, 1 (False)

    Yields:
    The next Fibonacci number in the sequence
    """
    if start_with_zero:
        a, b = 0, 1
    else:
        a, b = 1, 1

    for _ in range(n):
        yield a
        a, b = b, a + b

# Higher-order function
def create_multiplier(factor: int, add_value: int = 0) -> Callable[[int], int]:
    """
    Higher-order function that creates and returns another function - UPDATED with add_value parameter.

    Args:
    factor: The multiplication factor
    add_value: Value to add after multiplication

    Returns:
    A function that multiplies its input by the factor and adds the add_value
    """
    def multiplier(x: int) -> int:
        return x * factor + add_value

    return multiplier

# Lambda expression assigned to a variable
square = lambda x: x * x

# Function with type variables
def first_item_or_default(items: List[T], default: T) -> T:
    """
    Return the first item from a list or a default value if the list is empty.

    Args:
        items: List of items of type T
        default: Default value of type T

    Returns:
        First item or default
    """
    return items[0] if items else default

# Recursive function
def factorial(n: int) -> int:
    """
    Calculate factorial using recursion.

    Args:
        n: The number to calculate factorial for

    Returns:
        The factorial of n
    """
    if n <= 1:
        return 1
    return n * factorial(n - 1)