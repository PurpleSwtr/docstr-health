import inspect

from cli.cli import RichOutput
from core.config import config
from core.enums import StatusDocstring
from models import PythonFunction, PythonModule


class BaseChecker:
    def __init__(self, module: PythonModule) -> None:
        self.module = module
        self.output = RichOutput()


class DocstringChecker(BaseChecker):
    def check_module(self):
        print(str(f"| {self.module} |").center(32, "-"))
        for func in self.module.functions_to_check:
            self.display_func_status(func)
        print("\n")

    def display_func_status(self, func: PythonFunction):
        status = self.inspect_func_status(func)
        self.output.func_docstring_status(func_name=func.name, status=status)

    @staticmethod
    def inspect_func_status(func: PythonFunction) -> StatusDocstring:
        docstring = func.get_docstring()
        if not docstring:
            return StatusDocstring.BAD

        if any(req in docstring for req in config.requires["epic"]):
            return StatusDocstring.EPIC
        if any(req in docstring for req in config.requires["special"]):
            return StatusDocstring.SPECIAL

        return StatusDocstring.GOOD


class TestCoverageChecker(BaseChecker): ...
