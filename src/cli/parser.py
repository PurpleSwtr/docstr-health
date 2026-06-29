import argparse
from pathlib import Path


def get_parser():
    parser = argparse.ArgumentParser(
        prog="PyCoverageAnalyzer", description="Проверка docstring и тестов."
    )

    parser.add_argument(
        "project_path",
        type=Path,
        help="Путь к директории для проверки",
    )

    parser.add_argument(
        "--compact",
        action="store_true",
        help="Выводить только общую статистику, скрывая список функций.",
    )

    return parser
