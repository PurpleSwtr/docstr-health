from pathlib import Path


class DocstrHealthError(Exception): ...


class GitNotInstalledError(DocstrHealthError):
    def __init__(
        self,
        message="Git are not installed on this machine. Please, install git before running this command.",
    ):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


class PythonParseError(DocstrHealthError):
    """Raised when a Python file cannot be parsed."""

    def __init__(self, file_path: Path, reason: Exception):
        self.file_path = file_path
        self.reason = reason
        super().__init__(f"{file_path}: {reason}")


class PythonFilesNotFound(DocstrHealthError):
    """Raised when no Python files were found"""

    def __init__(
        self,
        message="There are no .py files in the directory being checked.",
    ):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


class DirectoryNotFoundError(DocstrHealthError):
    def __init__(self, path: Path):
        self.path = path
        super().__init__(f"Directory not found: {path}")

    def __str__(self):
        return f"Directory not found: {self.path}"


class NotADirectoryPathError(DocstrHealthError):
    def __init__(self, path: Path):
        self.path = path
        super().__init__(f"Not a directory: {path}")

    def __str__(self):
        return f"Not a directory: {self.path}"
