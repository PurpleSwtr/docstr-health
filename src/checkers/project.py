from collections import Counter
from pathlib import Path

from checkers.docstring import DocstringChecker
from models.module import PythonModule
from models.report import ModuleReport


class ProjectChecker:
    def __init__(self, target_dir: Path, excluded: list[str]) -> None:
        self._target_dir = target_dir
        self._excluded = excluded
        self._python_files = self._scan_python_files()
        self.modules = [PythonModule(file_path=file) for file in self._python_files]
        self._reports: list[ModuleReport] = []

    def get_quantity_of_func_type(self) -> dict:
        counters = [
            Counter(report.get_func_type_quantity()) for report in self._reports
        ]
        total_counter = sum(counters, Counter())
        return dict(total_counter)

    def _get_count_modules(self) -> int:
        return len(self.modules)

    def _get_statuses_stat(self) -> Counter:
        statuses: list = [report.module_status for report in self._reports]
        return Counter(statuses)

    def docstring_check(self):
        for module in self.modules:
            checker = DocstringChecker(module)
            module_report = checker.check_module()
            self._reports.append(module_report)

    def _scan_python_files(self) -> list[Path]:
        result: list[Path] = []
        for file_path in self._target_dir.rglob("*.py"):
            if not any(word in str(file_path) for word in self._excluded):
                result.append(file_path)
        return result
