from typing import Any


class TestDTO:
    """The TestDTO class."""

    def __init__(self, status: str):
        """Initialize a new instance of the TestDTO class."""
        self.status = status
        self._validate()

    def __repr__(self) -> str:
        """Return the string representation of the TestDTO object."""
        return f"testlDTO(status={self.status})"

    def _validate(self) -> None:
        """Validate the TestDTO object."""
        if not isinstance(self.status, str):
            raise ValueError("Status must be a string")


def test_method_handler(self: Any) -> TestDTO:
    """TEST DESCRIPTION."""
    print("This is a test method handler")
    return TestDTO(status="success")
