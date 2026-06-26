import ast
from functools import wraps
from typing import Callable

from rich.text import Text

from cli.cli import RichOutput
from core.config import config
from core.enums import StatusDocstring, StatusTypechecking
from models import PythonFunction, PythonModule


class BaseChecker:
    def __init__(self, module: PythonModule) -> None:
        self.module = module
        self.output = RichOutput()

    def displayed_module(self, func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(str(f"| {self.module} |").center(32, "-"))
            res = func(*args, **kwargs)
            return res

        return wrapper


class DocstringChecker(BaseChecker):
    def __init__(self, module: PythonModule) -> None:
        super().__init__(module)
        self.inspected_statuses = {"bad": 0, "good": 0, "special": 0, "epic": 0}

    @property
    def total_inspected_statuses(self):
        return sum(status for status in list(self.inspected_statuses.values()))

    def display_statistics(self):
        for status, value in self.inspected_statuses.items():
            print(status, value)

        # self.output.display_panel(
        #         text=inspected_functions,
        #         title=str(self.module),
        #         panel_status=panel_status,
        #     )

    def check_module(self):
        inspected_functions = []

        for func in self.module.functions_to_check:
            inspected_functions.append(self.get_func_status_text(func))

        panel_status = self.module_status

        if inspected_functions:
            self.output.display_panel(
                text=inspected_functions,
                title=str(self.module),
                panel_status=panel_status,
            )
        self.display_statistics()
        print("\n")

    @property
    def module_status(self) -> str:
        """
        Статус по модулю рассчитывается по следующей схеме:
        Все bad -> bad
        Есть bad (но не все) -> warning
        Нет bad + epic > 50% -> epic
        Нет bad + special > 50% -> special
        Нет bad и редкостей мало -> good

        Округление в меньшую сторону в случае равенства special и epic.
        """
        total = self.total_inspected_statuses
        statuses = self.inspected_statuses

        if statuses["bad"] == total or statuses["bad"] > 0.5 * total:
            return "bad"

        if statuses["bad"] > 0:
            return "warning"

        if statuses["epic"] > 0.5 * total:
            return "epic"
        if (
            statuses["special"] > 0.5 * total
            or statuses["special"] == statuses["epic"]
            and statuses["special"] > 0
            and statuses["epic"] > 0
        ):
            return "special"

        return "good"

    def get_statistics_text(self): ...

    def get_func_status_text(self, func: PythonFunction) -> Text:
        status = self.inspect_func_status(func)
        return self.output.func_docstring_status(func_name=func.name, status=status)

    def inspect_func_status(self, func: PythonFunction) -> StatusDocstring:
        docstring = func.get_docstring()
        if not docstring:
            self.inspected_statuses["bad"] += 1
            return StatusDocstring.BAD

        if any(req in docstring for req in config.requires["epic"]):
            self.inspected_statuses["epic"] += 1
            return StatusDocstring.EPIC
        if any(req in docstring for req in config.requires["special"]):
            self.inspected_statuses["special"] += 1
            return StatusDocstring.SPECIAL

        self.inspected_statuses["good"] += 1
        return StatusDocstring.GOOD


class TestCoverageChecker(BaseChecker): ...


# В дальнейшем можно придумать что-то такое, пока что набросал прототипчик
class TypeChecker(BaseChecker):
    @staticmethod
    def inspect_func_type_checking(func: PythonFunction) -> StatusTypechecking:
        for arg in func._ast_node.args.args:
            if arg.annotation:
                ann_str = ast.unparse(arg.annotation)
            else:
                return StatusTypechecking.ARGS

        if func._ast_node.returns:
            ann_str = ast.unparse(func._ast_node.returns)
        else:
            return StatusTypechecking.RETURN
