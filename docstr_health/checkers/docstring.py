from rich.text import Text

from ..checkers.base import BaseChecker
from ..core.config import config
from ..core.enums import StatusDocstring
from ..core.settings import AppSettings
from ..models.function import PythonFunction
from ..models.module import PythonModule
from ..models.report import ModuleReport


class DocstringChecker(BaseChecker):
    def __init__(self, module: PythonModule, settings: AppSettings) -> None:
        super().__init__(module)
        self.inspected_statuses = {
            "bad": 0,
            "good": 0,
            "special": 0,
            "epic": 0,
            "skipped": 0,
        }
        self.settings: AppSettings = settings
        self._func_statuses: dict[int, StatusDocstring] = {}
        self._module_doc_status: StatusDocstring | None = None

    @property
    def total_inspected_statuses(self):
        return sum(status for status in list(self.inspected_statuses.values()))

    def get_statistics(self, report: ModuleReport) -> list[Text]:
        statistics = []
        statistics.append(Text("Statistics:", justify="center"))
        for status, value in self.inspected_statuses.items():
            if value > 0:
                symbol = config.parameters[f"{status}_symbol"]
                color = config.parameters[f"{status}_color"]
                statistics.append(Text(f"{symbol} {status} - {value}", style=color))

        avg_len = report.average_docstring_length
        med_len = report.median_docstring_length
        longest = report.longest_docstring

        statistics.append(Text(f"Avg length: {avg_len:.1f} words", style="cyan"))
        statistics.append(Text(f"Median length: {med_len:.1f} words", style="cyan"))
        if longest:
            statistics.append(Text(f"Longest: {longest[0]} ({longest[1]} words)", style="cyan"))
        else:
            statistics.append(Text("Longest: N/A", style="cyan"))

        return statistics
        # self.output.display_panel(
        #         text=inspected_functions,
        #         title=str(self.module),
        #         panel_status=panel_status,
        #     )

    def check_module(self) -> ModuleReport | None:
        functions_to_check = self.module.functions_to_check
        if not functions_to_check:
            return None

        if self.settings.doc_check:
            module_docstring = self.module.get_module_docstring()
            self._module_doc_status = self.check_docstring(module_docstring)

        docstring_lengths = []
        for func in functions_to_check:
            self._func_statuses[id(func)] = self.inspect_func_status(func)
            docstring = func.get_docstring()
            if docstring:
                docstring_lengths.append((func.name, len(docstring.split())))

        report = ModuleReport(
            module_status=self.module_status,
            inspected_functions=functions_to_check,
            docstring_lengths=docstring_lengths,
        )

        if not self.settings.compact:
            self._display(report)

        return report

    def _display(self, report: ModuleReport):
        inspected = [Text("Inspected:", justify="center")]

        if self.settings.doc_check and self._module_doc_status is not None:
            inspected.append(
                self.output.func_docstring_status(
                    func_name="__doc__",
                    status=self._module_doc_status,
                )
            )

        for func in report.inspected_functions:
            inspected.append(self.get_func_status_text(func))

        statistics = self.get_statistics(report)
        self.output.display_panel(
            text=[inspected, statistics],
            title=str(self.module),
            panel_status=self.module_status,
        )

    @property
    def module_status(self) -> str:
        """
        Module status is calculated as follows:
        All bad                     -> bad
        Some bad (not all)          -> warning
        No bad + epic > 50%         -> epic
        No bad + special > 50%      -> special
        No bad, few special/epic    -> good

        Rounds down when special and epic are tied.
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

    def inspect_func_status(self, func: PythonFunction) -> StatusDocstring:
        """Checking the state of a function docstring."""
        docstring = func.get_docstring()
        return self.check_docstring(docstring)

    def get_func_status_text(self, func: PythonFunction) -> Text:
        status = self._func_statuses[id(func)]
        return self.output.func_docstring_status(func_name=func.name, status=status)

    def check_docstring(self, docstring: str | None) -> StatusDocstring:
        """Evaluate the quality of a docstring and assign a status.

        The evaluation follows a priority based on content presence
        and keyword matching:
            1. BAD: Docstring is missing or empty.
            2. GOOD: Has content but lacks EPIC/SPECIAL keywords.
            3. SPECIAL: Contains basic parameter keywords.
            4. EPIC: Contains advanced keywords.

        This method also increments the corresponding counter in
        ``self.inspected_statuses``.

        Args:
            docstring: The docstring text to evaluate, or None.

        Returns:
            StatusDocstring: The matched status enum value.
        """
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
