from rich.text import Text

from checkers.base import BaseChecker
from core.config import config
from core.enums import StatusDocstring
from models.function import PythonFunction
from models.module import PythonModule
from models.report import ModuleReport


class DocstringChecker(BaseChecker):
    def __init__(self, module: PythonModule) -> None:
        super().__init__(module)
        self.inspected_statuses = {"bad": 0, "good": 0, "special": 0, "epic": 0}

    @property
    def total_inspected_statuses(self):
        return sum(status for status in list(self.inspected_statuses.values()))

    def get_statistics(self) -> list[Text]:
        statistics = []
        statistics.append(Text("Statistics:", justify="center"))
        for status, value in self.inspected_statuses.items():
            if value > 0:
                symbol = config.parameters[f"{status}_symbol"]
                color = config.parameters[f"{status}_color"]
                statistics.append(Text(f"{symbol} {status} - {value}", style=color))
        return statistics
        # self.output.display_panel(
        #         text=inspected_functions,
        #         title=str(self.module),
        #         panel_status=panel_status,
        #     )

    def check_module(self) -> ModuleReport:
        inspected_functions = []

        for func in self.module.functions_to_check:
            inspected_functions.append(self.get_func_status_text(func))

        panel_status = self.module_status

        statistics = self.get_statistics()
        content = []

        content.append(inspected_functions)
        content.append(statistics)

        if inspected_functions:
            self.output.display_panel(
                text=content,
                title=str(self.module),
                panel_status=panel_status,
            )
        print("\n")

        return ModuleReport(module_status=self.module_status)

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
