from argparse import Namespace

from core.config import config


class AppSettings:
    def __init__(
        self,
        doc_check: bool = False,
        compact: bool = False,
        repo_url: str | None = None,
        cache_dir: str | None = None,
        excluded: list[str] | None = None,
    ) -> None:
        self.doc_check = doc_check
        self.compact = compact
        self.repo_url = repo_url
        self.cache_dir = cache_dir or config.get_cache_dir()
        self.excluded = excluded or config.excluded

    @classmethod
    def from_args(cls, args: Namespace) -> AppSettings:
        return cls(
            doc_check=args.doc_modules,
            compact=args.compact,
            repo_url=args.repo_url,
        )
