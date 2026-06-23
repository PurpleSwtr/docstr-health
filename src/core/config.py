import tomllib
from pathlib import Path

ROOT: Path = Path(__file__).resolve().parent.parent.parent


class Config:
    def __init__(self) -> None:
        self.excluded_directories = self.parameters.get("excluded_directories", [])

    @property
    def parameters(self) -> dict:
        with open(ROOT / "config.toml", "rb") as f:
            data = tomllib.load(f)
        return data.get("user_parameters", {})


config = Config()
