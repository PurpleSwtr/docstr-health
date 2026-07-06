import tomllib
from pathlib import Path

_ROOT: Path = Path(__file__).resolve().parent.parent.parent
_BASE_CACHE_DIR = Path.home() / ".cache" / "docstring-test-checker"
_REPOS_DIR = _BASE_CACHE_DIR / "repos"
_LOGS_DIR = _BASE_CACHE_DIR / "logs"


class Config:
    def __init__(self) -> None:
        self.excluded = self.parameters.get("excluded", [])

    @staticmethod
    def get_cache_dir() -> Path:
        return _REPOS_DIR

    @staticmethod
    def get_logs_dir() -> Path:
        return _LOGS_DIR

    @staticmethod
    def get_sorted_statuses() -> list[str]:
        return ["bad", "warning", "good", "special", "epic"]

    @staticmethod
    def get_sorted_general_stat() -> list[str]:
        return [
            "modules",
            "class",
            "function",
            "async function",
            "total",
        ]

    @property
    def data(self) -> dict:
        """
        Основной интерфейс для получения данных из конфигурации.
        """
        with open(_ROOT / "config.toml", "rb") as f:
            return tomllib.load(f)

    @property
    def requires(self) -> dict:
        """
        Свойство требований для получения функциями особых статусов
        """
        return self.data.get("requires_v3", {})

    @property
    def parameters(self) -> dict:
        return self.data.get("user_parameters", {})

    def ensure_directories(self) -> None:
        """
        Создает все необходимые директории для работы приложения.
        """
        self.get_cache_dir().mkdir(parents=True, exist_ok=True)
        self.get_logs_dir().mkdir(parents=True, exist_ok=True)


config = Config()

config.ensure_directories()
