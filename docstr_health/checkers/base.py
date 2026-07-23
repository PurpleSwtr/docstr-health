from abc import ABC, abstractmethod

from ..cli.cli import RichOutput
from ..models.module import PythonModule
from ..models.report import ModuleReport


class BaseChecker(ABC):
    _shared_output: RichOutput | None = None

    def __init__(self, module: PythonModule) -> None:
        self.module = module
        if BaseChecker._shared_output is None:
            BaseChecker._shared_output = RichOutput()
        self.output = BaseChecker._shared_output

    @abstractmethod
    def check_module(self) -> ModuleReport | None:
        """Check the module and return a report.

        Subclasses must implement this method to define
        module-level analysis logic.

        Returns:
            ModuleReport: Report with all metrics for statistics.
        """
