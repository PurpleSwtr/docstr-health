import tomllib
from importlib import metadata
from pathlib import Path

_PACKAGE_ROOT: Path = Path(__file__).resolve().parent.parent

_BASE_CACHE_DIR = Path.home() / ".cache" / "docstr-health"
_REPOS_DIR = _BASE_CACHE_DIR / "repos"
_LOGS_DIR = _BASE_CACHE_DIR / "logs"


class Config:
    def __init__(self) -> None:
        self.excluded = self.parameters.get("excluded", [])
        self._cache_dir = _REPOS_DIR

    def get_cache_dir(self) -> Path:
        return Path(self._cache_dir)

    def set_cache_dir(self, dir: Path) -> None:
        self._cache_dir = dir

    @staticmethod
    def get_logs_dir() -> Path:
        return _LOGS_DIR

    @staticmethod
    def get_sorted_statuses() -> list[str]:
        return ["bad", "warning", "good", "special", "epic"]

    @staticmethod
    def get_version() -> str:
        try:
            return metadata.version("docstr-health")
        except metadata.PackageNotFoundError:
            pyproject_path = _PACKAGE_ROOT.parent / "pyproject.toml"
            if pyproject_path.exists():
                with open(pyproject_path, "rb") as f:
                    data = tomllib.load(f)
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

    @property
    def data(self) -> dict:
        """The main interface for obtaining data from the configuration."""
        config_path = _PACKAGE_ROOT / "config.toml"
        with open(config_path, "rb") as f:
            return tomllib.load(f)

    @property
    def requires(self) -> dict:
        return self.data.get("requires_v4", {})

    @property
    def parameters(self) -> dict:
        return self.data.get("user_parameters", {})

    def ensure_directories(self) -> None:
        self.get_cache_dir().mkdir(parents=True, exist_ok=True)
        self.get_logs_dir().mkdir(parents=True, exist_ok=True)


config = Config()
