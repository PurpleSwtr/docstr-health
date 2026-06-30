from pathlib import Path

from .base import BaseSource


class LocalSource(BaseSource):
    """Local directory."""

    def __init__(self, path: Path) -> None:
        self._path = path

    def get_path(self) -> Path:
        if not self._path.exists():
            raise FileNotFoundError(f"Directory not found: {self._path}")
        if not self._path.is_dir():
            raise NotADirectoryError(f"Not a directory: {self._path}")
        return self._path

    def cleanup(self) -> None:
        pass
