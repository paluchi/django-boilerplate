from dataclasses import dataclass
from typing import Any


@dataclass
class TestDTO:
    """The TestDTO class."""

    status: str

    def __post_init__(self):
        """Validate the TestDTO object."""
        if not isinstance(self.status, str):
            raise ValueError("Status must be a string")


def test_method_handler(self: Any, yourText: str) -> Any:
    """TEST DESCRIPTION."""

    print("This is a test method handler", yourText)
    return TestDTO(status="success")
