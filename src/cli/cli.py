from rich import print as rich_print
from rich.console import Console, Group
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

from core.config import config
from core.enums import StatusDocstring


class RichOutput:
    def __init__(self) -> None:
        self.console = Console()
        # self.text = ""
        self.color = "common"

    def set_color(self, color: str):
        self.color = color

    def cprint(self, text: Text):
        self.console.print(text)

    def func_docstring_status(self, func_name: str, status: StatusDocstring) -> Text:
        symbol = config.parameters[f"{status.value}_symbol"]
        color = config.parameters[f"{status.value}_color"]

        self.set_color(color)

        return Text(f" - {symbol} {func_name}", style=self.color)

    def display_panel(
        self, text: list[list[Text]], title: str, panel_status: str = "common"
    ):
        symbol = config.parameters[f"{panel_status}_symbol"]
        subtitle = f"{symbol} {panel_status} {symbol}"
        border_style = config.parameters[f"{panel_status}_color"]

        render: list = []

        for i, block in enumerate(text):
            render.extend(block)

            if i < len(text) - 1:
                render.append(Rule(style="dim"))

        content = Group(*render)

        rich_print(
            Panel.fit(
                content,
                title=title,
                subtitle=subtitle,
                border_style=border_style,
            )
        )

    @staticmethod
    def _get_style(value: str):
        return config.parameters[f"{value}_color"]

    @staticmethod
    def _get_symbol(value: str):
        return config.parameters[f"{value}_symbol"]

    def get_status_with_symbol(self, status: str) -> str:
        return f"{self._get_symbol(status)} {status}"

    @staticmethod
    def prepare_dict_table(
        data: dict, sorting_reference: list | None = None
    ) -> list[tuple]:
        """
        Converts a dictionary to a list of (key, value) tuples.

        Args:
            data: The original dictionary.
            order: If supplied, sorts by this order.
        """
        items = data.items()
        if sorting_reference:
            items = sorted(items, key=lambda item: sorting_reference.index(item[0]))
        return [(str(k), str(v)) for k, v in items]

    @staticmethod
    def _sort_statuses(statuses: list) -> list:
        return sorted(statuses, key=config.get_sorted_statuses().index)

    def display_table(self, title: str, headers: list[str], data: dict):
        table = Table(title=title)
        for header in headers:
            table.add_column(header, justify="center")

        table_data = self.prepare_dict_table(data, config.get_sorted_statuses())

        for status, count in table_data:
            status_text = Text(
                self.get_status_with_symbol(status=status),
                style=self._get_style(status),
                justify="left",
            )
            table.add_row(status_text, str(count))

        self.console.print(table)
