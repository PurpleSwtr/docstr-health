import subprocess
from pathlib import Path

from core.config import config
from sources.base import BaseSource


class PyPiPackageSource(BaseSource):
    """Remote PyPi package."""

    def __init__(self, package_url: str) -> None:
        self._package_url = package_url

    def get_download_method(self) -> list[str]:
        if config.parameters["use_uv"]:
            return ["uv", "pip", "install"]
        else:
            return ["pip", "install"]

    @property
    def cache_path(self) -> Path:
        return config.get_cache_dir() / self._package_url

    def get_from_cache(self) -> Path | None:
        if self.cache_path.is_dir() and any(self.cache_path.iterdir()):
            return self.cache_path
        return None

    def get_from_package(self):
        download_method = self.get_download_method()
        subprocess.run(
            [
                *download_method,
                self._package_url,
                "--target",
                str(self.cache_path),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        return self.cache_path

    def get_path(self) -> Path | None:
        cached = self.get_from_cache()
        if cached is not None:
            return cached
        return self.get_from_package()

    def cleanup(self) -> None: ...
