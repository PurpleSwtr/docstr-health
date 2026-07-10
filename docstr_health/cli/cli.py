from rich import print as rich_print
from rich.console import Console, Group
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

from ..core.config import config
from ..core.enums import StatusDocstring


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
                padding=(1, 2),
            )
        )
        print("\n")

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
        items = list(data.items())
        if sorting_reference:
            items = sorted(items, key=lambda item: sorting_reference.index(item[0]))
        return [(str(k), str(v)) for k, v in items]

    @staticmethod
    def _sort_statuses(statuses: list) -> list:
        return sorted(statuses, key=config.get_sorted_statuses().index)

    def get_table(
        self,
        title: str,
        headers: list[str],
        data: dict,
        sorting_reference: list | None = None,
        last_line_separator: bool = False,
    ) -> Table:
        table = Table(title=title)

        for header in headers:
            table.add_column(header, justify="center")

        table_data = self.prepare_dict_table(data, sorting_reference)

        style = ""
        end_section = False

        total_rows = len(table_data)
        total = 0
        if 'total' in data:
            total = data['total']
        else: 
            total = sum([cnt for _, cnt in data.items()])

        for i, (status, count) in enumerate(table_data):
            # last line check
            if i == total_rows - 2 and last_line_separator:
                end_section = True
            if status in config.get_sorted_statuses():
                style = self._get_style(status)
                status = self.get_status_with_symbol(status=status)
            status_text = Text(
                status,
                style=style,
                justify="left",
            )
            percentage = round(int(count) / total * 100, 1)
            table.add_row(status_text, str(count), f'{percentage}%', end_section=end_section)
        return table
