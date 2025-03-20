"""
Test file with a class that will have methods deleted.
"""

class TestMethodDeletion:
    """Class for testing method deletion."""

    def __init__(self, name: str):
        self.name = name

    def method_to_keep(self) -> str:
        """This method will be kept."""
        return f"Method kept for {self.name}"

    def another_method_to_keep(self) -> str:
        """This method will also be kept."""
        return f"Another method kept for {self.name}"