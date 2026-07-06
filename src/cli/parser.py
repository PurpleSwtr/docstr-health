import argparse
from pathlib import Path

from core.config import config


def get_parser():
    parser = argparse.ArgumentParser(
        prog="PyCoverageAnalyzer", description="Проверка docstring и тестов."
    )

    parser.add_argument(
        "project_path",
        type=Path,
        nargs="?",
        default=".",
        help="Путь к директории для проверки",
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
        "--repo-url",
        type=str,
        help="Просканировать проект из удалённого репозитория.",
    )

    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=config.get_cache_dir(),
        help=f"Directory for cached repositories (default: {config.get_cache_dir()})",
    )

    # parser.add_argument(
    #     "--details-skipped",
    # )

    return parser
