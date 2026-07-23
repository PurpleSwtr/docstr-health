from __future__ import annotations

from argparse import Namespace
from pathlib import Path

from ..core.config import config


class AppSettings:
    def __init__(
        self,
        doc_check: bool = False,
        compact: bool = False,
        no_cache: bool = False,
        ignore_tests: bool = False,
        short_names: bool = False,
        repo_url: str | None = None,
        pypi_package: str | None = None,
        threshold_warning: int | None = None,
        threshold_special: int | None = None,
        threshold_epic: int | None = None,
        cache_dir: Path | None = None,
        excluded: list[str] | None = None,
    ) -> None:
        self.doc_check = doc_check
        self.compact = compact
        self.no_cache = no_cache
        self.ignore_tests = ignore_tests
        self.short_names = short_names
        self.repo_url = repo_url
        self.pypi_package = pypi_package
        self.threshold_warning = threshold_warning
        self.threshold_special = threshold_special
        self.threshold_epic = threshold_epic
        self.cache_dir = cache_dir or config.get_cache_dir()
        self.excluded = excluded or config.excluded

    # @staticmethod
    # def

    @classmethod
    def from_args(cls, args: Namespace) -> AppSettings:
        return cls(
            doc_check=args.doc_modules,
            compact=args.compact,
            short_names=args.short_names,
            no_cache=args.no_cache,
            repo_url=args.repo_url,
            pypi_package=args.pypi_package,
            threshold_warning=args.threshold_warning,
            threshold_special=args.threshold_special,
            threshold_epic=args.threshold_epic,
            cache_dir=args.cache_dir,
            ignore_tests=args.ignore_tests,
        )
