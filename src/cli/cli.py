from rich import print as rich_print
from rich.console import Console, Group
from rich.panel import Panel
from rich.text import Text

from core.config import config
from core.enums import StatusDocstring


class RichOutput:
    def __init__(self) -> None:
        self.console = Console()
        # self.text = ""
        self.color = "white"

    def set_color(self, color: str):
        self.color = color

    def cprint(self, text: Text):
        self.console.print(text)

    def func_docstring_status(self, func_name: str, status: StatusDocstring) -> Text:
        symbol = config.parameters[f"{status.value}_symbol"]
        color = config.parameters[f"{status.value}_color"]

        self.set_color(color)

        return Text(f" - {symbol} {func_name}", style=self.color)

    def display_panel(self, text: list[Text], title: str, panel_status: str = "white"):
        content = Group(*text)
        symbol = config.parameters[f"{panel_status}_symbol"]
        subtitle = None
        if panel_status != "white":
            subtitle = f"{symbol} {panel_status} {symbol}"
        rich_print(
            Panel.fit(
                content,
                title=title,
                subtitle=subtitle,
                border_style=config.parameters[f"{panel_status}_color"],
            )
        )


ro = RichOutput()
