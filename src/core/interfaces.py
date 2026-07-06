from typing import Protocol


class Checkable(Protocol):
    """Contract for verification purposes."""

    @property
    def name(self) -> str: ...
    def get_docstring(self) -> str | None: ...
