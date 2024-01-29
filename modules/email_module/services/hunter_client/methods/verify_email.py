from typing import Any


class EmailDTO:
    """The EmailDTO class."""

    def __init__(self, status: str, score: float, disposable: bool, **kwargs: Any):
        """Initialize a new instance of the EmailDTO class."""
        self.status = status
        self.score = float(score)
        self.disposable = disposable
        self._validate()

    def __repr__(self) -> str:
        """Return the string representation of the EmailDTO object."""
        class_name = "VerifyEmailDTO"
        status_repr = f"status={self.status}"
        score_repr = f"score={self.score}"
        disposable_repr = f"disposable={self.disposable}"
        return f"{class_name}({status_repr}, {score_repr}, {disposable_repr})"

    def _validate(self) -> None:
        """Validate the EmailDTO object."""
        if not isinstance(self.status, str):
            raise ValueError("Status must be a string")
        if not isinstance(self.score, float):
            raise ValueError("Score must be a float")
        if not isinstance(self.disposable, bool):
            raise ValueError("Disposable must be a boolean")
