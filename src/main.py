import argparse
from pathlib import Path

from core.config import config
from models import PythonModule


def scan_dir(folder_path: Path, excluded_directories: list) -> list[Path]:
    """Тут хоть чёто есть"""
    result: list[Path] = []
    for file_path in folder_path.rglob("*.py"):
        if not any(word in str(file_path) for word in excluded_directories):
            result.append(file_path)

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Проверка docstring и тестов.")

    parser.add_argument(
        "project_path",
        type=Path,
        help="Путь к директории для проверки",
    )

    args = parser.parse_args()

    target_dir = args.project_path
    excluded_directories = config.excluded_directories

    python_files = scan_dir(target_dir, excluded_directories)

    modules = [PythonModule(file_path=file) for file in python_files]

    # python_functions = map(lambda x: get_functions(x), python_files)

    all_functions_checked = [
        function
        for module in modules
        for function in module.functions
        if not function.is_dunder
    ]

    print(
        f"Найдено: {len(all_functions_checked)} функций: {', '.join(func.name for func in all_functions_checked)}"
    )
    print(
        f"Докстринги написаны для: {sum(func.has_docstring for func in all_functions_checked)}/{len(all_functions_checked)}"
    )
