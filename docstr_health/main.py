import sys
from contextlib import contextmanager
from io import TextIOWrapper
from typing import cast

from rich import print as rich_print
from rich.columns import Columns

from .checkers.project import ProjectChecker
from .cli.cli import RichOutput
from .cli.parser import get_parser
from .cli.progress_bar import progress_bar
from .core.config import config
from .core.logger import logger
from .core.settings import AppSettings
from .sources import get_repository_source


@contextmanager
def spacing():
    print()
    yield


def main():
    cast(TextIOWrapper, sys.stdout).reconfigure(encoding="utf-8", errors="replace")
    cast(TextIOWrapper, sys.stderr).reconfigure(encoding="utf-8", errors="replace")

    parser = get_parser()
    args = parser.parse_args()

    if args.project_path:
        args.project_path = args.project_path.resolve()
    if args.cache_dir:
        args.cache_dir = args.cache_dir.resolve()

    config.ensure_directories()
    settings = AppSettings.from_args(args)

    if settings.cache_dir:
        config.set_cache_dir(settings.cache_dir)

    logger.debug(config.get_cache_dir())

    source = get_repository_source(settings, args)

    project_checker = ProjectChecker(source=source, settings=settings)

    if project_checker.modules:
        start_module_name = project_checker.modules[0].file_path.name
    else:
        start_module_name = "No modules found"

    with progress_bar() as pg:
        _task = pg.add_task(
            "Checking...",
            total=len(project_checker.modules),
            module_name=start_module_name,
        )

        for task in project_checker.docstring_check():
            pg.update(_task, advance=1, module_name=task.file_path.name)

    statuses = project_checker.get_statuses_stat()

    general_stat_data = project_checker.get_quantity_of_func_type()
    if args.doc_modules:
        general_stat_data["modules"] = project_checker.get_count_modules()
    general_stat_data["total"] = sum(general_stat_data.values())

    renderer = RichOutput()

    tables_to_display = []

    tables_to_display.append(
        renderer.get_table(
            title="General statistics",
            headers=["Metric", "Value"],
            data=general_stat_data,
            sorting_reference=config.get_sorted_general_stat(),
            last_line_separator=True,
        )
    )
    tables_to_display.append(
        renderer.get_table(
            title="Number of modules each status",
            headers=["Module status", "Quantity"],
            data=statuses,
            sorting_reference=config.get_sorted_statuses(),
        )
    )

    skipped = {p.name: e for p, e in project_checker.skipped_modules}
    if skipped:
        tables_to_display.append(
            renderer.get_table(
                title="Skipped modules",
                headers=["Module", "Error"],
                data=skipped,
            )
        )

    rich_print(Columns(tables_to_display))

    if settings.no_cache:
        source.cleanup()


if __name__ == "__main__":
    with spacing():
        sys.exit(main())
