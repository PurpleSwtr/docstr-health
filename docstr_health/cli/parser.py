import argparse
from pathlib import Path

from ..core import __version__
from ..core.config import config


def get_parser():
    parser = argparse.ArgumentParser(
        prog="docstr-health", description="Проверка docstring и тестов."
    )

    parser.add_argument(
        "project_path",
        type=Path,
        nargs="?",
        default=Path("."),
        help="Путь к директории для проверки",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show version and exit.",
    )

    main_group = parser.add_argument_group("basic parameters")

    main_group.add_argument(
        "--repo-url",
        type=str,
        help="Просканировать проект из удалённого Git репозитория.",
    )

    main_group.add_argument(
        "--pypi-url",
        type=str,
        help="Просканировать проект из удалённого PyPi пакета.",
    )

    main_group.add_argument(
        "--cache-dir",
        type=Path,
        default=config.get_cache_dir(),
        help=f"Directory for cached repositories (default: {config.get_cache_dir()})",
    )

    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Не сохранять кеш для удалённых репозиториев.",
    )

    parser.add_argument(
        "--compact",
        action="store_true",
        help="Выводить только общую статистику, скрывая список функций.",
    )

    parser.add_argument(
        "--doc-modules",
        action="store_true",
        help="Учитывать __doc__ самих файлов",
    )

    parser.add_argument(
        "--ignore-tests",
        action="store_true",
        help="Ignore Test Units",
    )

    # parser.add_argument(
    #     "--details-skipped",
    # )

    return parser
