from dataclasses import dataclass, field
from typing import Any


@dataclass
class EmailDTO:
    """The EmailDTO class."""

    status: str
    score: float
    disposable: bool
    additional_attributes: dict = field(default_factory=dict, repr=False)

    def __init__(self, status: str, score: float, disposable: bool, **kwargs: Any):
        """Initialize the EmailDTO with given parameters and any additional keyword arguments."""
        self.status = status
        self.score = float(score)
        self.disposable = disposable
        self.additional_attributes = kwargs
        self.__post_init__()

    def __post_init__(self) -> None:
        """Validate the EmailDTO object after initialization and handle additional kwargs."""
        if not isinstance(self.status, str):
            raise ValueError("Status must be a string")
        if not isinstance(self.score, float):
            raise ValueError("Score must be a float")
        if not isinstance(self.disposable, bool):
            raise ValueError("Disposable must be a boolean")

        # Set additional attributes
        for key, attr_value in self.additional_attributes.items():
            setattr(self, key, attr_value)

        # Clear the dictionary as its items are now attributes
        self.additional_attributes.clear()
