from contextlib import contextmanager

from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
)


@contextmanager
def progress_bar():
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.fields[module_name]:<20}"),
        BarColumn(bar_width=50),
        MofNCompleteColumn(),
        transient=True,
    ) as progress:
        yield progress
