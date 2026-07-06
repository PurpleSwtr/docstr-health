from collections import Counter
from pathlib import Path

from checkers.docstring import DocstringChecker
from core.exceptions import PythonParseError
from core.settings import AppSettings
from models.module import PythonModule
from models.report import ModuleReport
from sources.base import BaseSource


class ProjectChecker:
    def __init__(self, source: BaseSource, settings: AppSettings) -> None:
        self.source: BaseSource = source
        self.settings: AppSettings = settings
        self._python_files = self._scan_python_files()
        self.modules = [PythonModule(file_path=file) for file in self._python_files]
        self._reports: list[ModuleReport] = []
        self._skipped_modules: list[tuple[Path, str]] = []

    @property
    def _target_dir(self):
        return self.source.get_path()

    def get_quantity_of_func_type(self) -> dict:
        counters = [
            Counter(report.get_func_type_quantity()) for report in self._reports
        ]
        total_counter = sum(counters, Counter())
        return dict(total_counter)

    def _get_count_modules(self) -> int:
        return len(self._reports)

    def _get_statuses_stat(self) -> Counter:
        statuses: list = [report.module_status for report in self._reports]
        return Counter(statuses)

    def docstring_check(
        self,
    ):
        for module in self.modules:
            try:
                checker = DocstringChecker(module, settings=self.settings)
                module_report = checker.check_module()
                if module_report is not None:
                    self._reports.append(module_report)
            except PythonParseError as e:
                self._skipped_modules.append((module.file_path, str(e)))

    @property
    def skipped_modules(self) -> list[tuple[Path, str]]:
        return self._skipped_modules

    def _scan_python_files(self) -> list[Path]:
        result: list[Path] = []
        if self._target_dir:
            for file_path in self._target_dir.rglob("*.py"):
                if not any(word in str(file_path) for word in self.settings.excluded):
                    result.append(file_path)
            return result
        return []
