import statistics
from collections import Counter
from pathlib import Path
from typing import Generator

from ..checkers.docstring import DocstringChecker
from ..core.exceptions import PythonParseError
from ..core.settings import AppSettings
from ..models.module import PythonModule
from ..models.report import ModuleReport
from ..sources.base import BaseSource


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

    def get_count_modules(self) -> int:
        return len(self._reports)

    def get_statuses_stat(self) -> Counter:
        statuses: list = [report.module_status for report in self._reports]
        return Counter(statuses)

    def _get_all_docstring_lengths(self) -> list[tuple[str, int]]:
        all_lengths = []
        for report in self._reports:
            all_lengths.extend(report.docstring_lengths)
        return all_lengths

    def get_avg_docstring_length(self) -> float:
        docstrings = self._get_all_docstring_lengths()
        if not docstrings:
            return 0.0
        return float(statistics.mean(length for _, length in docstrings))

    def get_median_docstring_length(self) -> float:
        docstrings = self._get_all_docstring_lengths()
        if not docstrings:
            return 0.0
        return float(statistics.median(length for _, length in docstrings))

    def get_longest_docstring(self) -> tuple[str, int] | None:
        docstrings = self._get_all_docstring_lengths()
        if not docstrings:
            return None
        return max(docstrings, key=lambda x: x[1])

    def docstring_check(
        self,
    ) -> Generator[PythonModule, None, None]:
        for module in self.modules:
            try:
                checker = DocstringChecker(module, settings=self.settings)
                module_report = checker.check_module()
                if module_report is not None:
                    self._reports.append(module_report)
                # else:
                #     self._skipped_modules.append(
                #         (module.file_path, "No functions to check")
                #     )
            except PythonParseError as e:
                self._skipped_modules.append((module.file_path, str(e)))

            yield module

    @property
    def skipped_modules(self) -> list[tuple[Path, str]]:
        return self._skipped_modules

    def _scan_python_files(self) -> list[Path]:
        result: list[Path] = []
        if self._target_dir:
            for file_path in self._target_dir.rglob("*.py"):
                file_name = file_path.name.lower()
                path_str = str(file_path).lower()
                if self.settings.ignore_tests:
                    self.settings.excluded.append("test_")
                excluded = [word.lower() for word in self.settings.excluded]

                is_excluded = any(
                    file_name.startswith(excl) or excl in path_str for excl in excluded
                )

                if not is_excluded:
                    result.append(file_path)
            return result
        return []
