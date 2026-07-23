import tomllib
from importlib import metadata
from pathlib import Path
from typing import Any, Final

_PACKAGE_ROOT: Final[Path] = Path(__file__).resolve().parent.parent

_BASE_CACHE_DIR = Path.home() / ".cache" / "docstr-health"
_REPOS_DIR = _BASE_CACHE_DIR / "repos"
_LOGS_DIR = _BASE_CACHE_DIR / "logs"
_PYPROJECT_FILE = _PACKAGE_ROOT.parent / "pyproject.toml"


class Config:
    def __init__(self) -> None:
        self.pyproject_data = self._pyproject_data()
        self.data = self._data()
        self.parameters = self._parameters()
        self.requires = self._requires()
        self.excluded = self._excluded()
        self._cache_dir = _REPOS_DIR

    def get_cache_dir(self) -> Path:
        return Path(self._cache_dir)

    def set_cache_dir(self, dir: Path) -> None:
        self._cache_dir = dir

    @staticmethod
    def get_logs_dir() -> Path:
        return _LOGS_DIR

    @staticmethod
    def _get_pyproject_file() -> Path:
        return _PYPROJECT_FILE

    def _pyproject_data(self) -> dict[str, Any]:
        pyproject_path = self._get_pyproject_file()
        if pyproject_path.exists():
            with open(pyproject_path, "rb") as f:
                data = tomllib.load(f)
            return data
        else:
            return {}

    @staticmethod
    def get_sorted_statuses() -> list[str]:
        return ["bad", "warning", "good", "special", "epic"]

    def get_version(self) -> str:
        try:
            return metadata.version("docstr-health")
        except metadata.PackageNotFoundError:
            data = self.pyproject_data
            if data:
                return data.get("project", {}).get("version", "unknown")
            return "unknown"

    @staticmethod
    def get_sorted_general_stat() -> list[str]:
        return [
            "modules",
            "class",
            "function",
            "async function",
            "avg docstring length",
            "median docstring length",
            "longest docstring",
            "total",
        ]

    def _data(self) -> dict[str, Any]:
        """The main interface for obtaining data from the configuration."""
        config_path = _PACKAGE_ROOT / "config.toml"

        data = {}

        with open(config_path, "rb") as f:
            data = tomllib.load(f)

        pyproject_data = self.pyproject_data.get("tool", {}).get("docstr-health", {})

        if pyproject_data:
            data.setdefault("user_parameters", {}).update(pyproject_data)

        return data

    def _requires(self) -> dict[str, Any]:
        return self.data.get("requires_v4", {})

    def _parameters(self) -> dict[str, Any]:
        return self.data.get("user_parameters", {})

    def _excluded(self) -> list[str]:
        return self.parameters.get("excluded", [])

    def ensure_directories(self) -> None:
        self.get_cache_dir().mkdir(parents=True, exist_ok=True)
        self.get_logs_dir().mkdir(parents=True, exist_ok=True)


config = Config()
