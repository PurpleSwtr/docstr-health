from enum import Enum

from rich.console import Console
from rich.text import Text

from src.core.config import config


class StatusDocstring(Enum):
    BAD = "bad"
    GOOD = "good"
    SPECIAL = "special"


class RichOutput:
    def __init__(self) -> None:
        self.console = Console()
        self.text = ""
        self.color = "white"

    def set_color(self, color: str):
        self.color = color

    def cprint(self):
        self.console.print(self.text)

    def func_docstring_status(self, func: str, status: StatusDocstring):
        self.text = Text(f" - {config.parameters[f'{status.value}_symbol']} {func}")
        self.set_color(config.parameters[f"{status.value}_color"])
        self.text.stylize(self.color)
        self.cprint()


ro = RichOutput()

ro.func_docstring_status("__init__", StatusDocstring.BAD)
