from pathlib import Path

from ..core.exceptions import DirectoryNotFoundError, NotADirectoryPathError
from .base import BaseSource


class LocalSource(BaseSource):
    """Local directory."""

    def __init__(self, path: Path) -> None:
        self._path = path.resolve()

    def get_path(self) -> Path:
        if not self._path.exists():
            raise DirectoryNotFoundError(self._path)
        if not self._path.is_dir():
            raise NotADirectoryPathError(self._path)
        return self._path

    def cleanup(self) -> None:
        pass
