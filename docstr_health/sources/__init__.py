from .base import BaseSource
from .git_repo import GitRepositorySource
from .local import LocalSource
from .pypi_package import PyPiPackageSource


def get_repository_source(settings, args) -> BaseSource:
    if settings.repo_url:
        return GitRepositorySource(settings.repo_url)
    if settings.pypi_url:
        return PyPiPackageSource(settings.pypi_url)
    return LocalSource(args.project_path)
