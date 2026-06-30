import tomllib
from pathlib import Path

ROOT: Path = Path(__file__).resolve().parent.parent.parent


class Config:
    def __init__(self) -> None:
        self.excluded = self.parameters.get("excluded", [])

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
        with open(ROOT / "config.toml", "rb") as f:
            return tomllib.load(f)

    @property
    def requires(self) -> dict:
        """
        Свойство требований для получения функциями особых статусов
        """
        return self.data.get("requires_v2", {})

    @property
    def parameters(self) -> dict:
        return self.data.get("user_parameters", {})


config = Config()
