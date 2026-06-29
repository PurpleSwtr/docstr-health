from pathlib import Path

from checkers.docstring import DocstringChecker
from models.module import PythonModule


class ProjectChecker:
    def __init__(self, target_dir: Path, excluded: list[str]) -> None:
        self._target_dir = target_dir
        self._excluded = excluded
        self._python_files = self._scan_python_files()
        self.modules = [PythonModule(file_path=file) for file in self._python_files]
        self._reports = []

    # def get_statistic(self) -> list:
    #     for report in self._reports:
    #         print(len(report.module_status))

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
