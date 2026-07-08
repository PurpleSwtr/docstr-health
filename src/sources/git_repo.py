import shutil
import subprocess
from pathlib import Path

from core.config import config
from core.exceptions import GitNotInstalledError
from core.logger import logger
from sources.base import BaseSource


class GitRepositorySource(BaseSource):
    """Remote git repository."""

    def __init__(self, repo_url: str) -> None:
        self._repo_url = repo_url
        self.check_git_installed()

    @staticmethod
    def check_git_installed():
        if shutil.which("git") is None:
            raise GitNotInstalledError()

    @property
    def cache_path(self) -> Path:
        repo_name = self._repo_url.rstrip("/").split("/")[-1].removesuffix(".git")
        return config.get_cache_dir() / repo_name

    def get_from_cache(self) -> Path | None:
        if self.cache_path.is_dir() and any(self.cache_path.iterdir()):
            return self.cache_path
        return None

    def get_from_repo(self):
        subprocess.run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                self._repo_url,
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
        return self.get_from_repo()

    def cleanup(self) -> None:
        base = config.get_cache_dir()
        try:
            self.cache_path.relative_to(base)
        except ValueError as e:
            logger.warning(e)
            return

        if not self.cache_path.is_dir():
            return
