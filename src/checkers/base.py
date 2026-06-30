from abc import ABC, abstractmethod

from cli.cli import RichOutput
from models.module import PythonModule
from models.report import ModuleReport


class BaseChecker(ABC):
    def __init__(self, module: PythonModule) -> None:
        self.module = module
        self.output = RichOutput()

    @abstractmethod
    def check_module(self) -> ModuleReport:
        """Check the module and return a report.

        Subclasses must implement this method to define
        module-level analysis logic.

        Returns:
            ModuleReport: Report with all metrics for statistics.
        """
