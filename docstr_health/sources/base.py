from abc import ABC, abstractmethod
from pathlib import Path


class BaseSource(ABC):
    """Base class for data sources."""

    @abstractmethod
    def get_path(self) -> Path | None:
        """
        Returns the path to the directory to be analyzed.
        """
        ...

    @abstractmethod
    def cleanup(self) -> None:
        """Cleans up temporary files (if any)."""
        ...

    # def __init__(self) -> None:
    #     super().__init__()
    #     self._temp_dir_obj = tempfile.mkdtemp()

    # def __enter__(self):

    #     return self

    # def __exit__(self):
    #     pass
