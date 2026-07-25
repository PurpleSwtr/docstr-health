import sys
from contextlib import contextmanager

from rich import print as rich_print

from docstr_health.checkers.ci_failure import CiFailureChecker

from .checkers.project import ProjectChecker
from .cli.cli import RichOutput
from .cli.parser import get_parser
from .cli.runner import run_check
from .core.config import config
from .core.exceptions import DocstrHealthError
from .core.logger import logger
from .core.settings import AppSettings
from .sources import get_repository_source


@contextmanager
def spacing():
    print()
    yield


def main():
    parser = get_parser()
    args = parser.parse_args()

    if args.project_path:
        args.project_path = args.project_path.resolve()
    if args.cache_dir:
        args.cache_dir = args.cache_dir.resolve()

    config.ensure_directories()
    settings = AppSettings.from_args(args)
    renderer = RichOutput(quiet=config.parameters.get("ci", False))

    if settings.cache_dir:
        config.set_cache_dir(settings.cache_dir)

    logger.debug(config.get_cache_dir())

    source = get_repository_source(settings, args)

    project_checker = ProjectChecker(source=source, settings=settings)

    run_check(project_checker)

    statuses = project_checker.get_statuses_stat()
    project_report = project_checker.get_project_report()

    ci_checker = CiFailureChecker(project_report=project_report)
    ci_checker.assertion()

    general_stat_data = project_checker.get_quantity_of_func_type()
    if args.doc_modules:
        general_stat_data["modules"] = project_checker.get_count_modules()
    general_stat_data["total"] = sum(general_stat_data.values())

    tables_to_display = []

    tables_to_display.append(
        renderer.get_table(
            title="General statistics",
            headers=["Metric", "Value", "Rate"],
            data=general_stat_data,
            sorting_reference=config.get_sorted_general_stat(),
            last_line_separator=True,
        )
    )
    tables_to_display.append(
        renderer.get_table(
            title="Number of modules each status",
            headers=["Module status", "Quantity", "Rate"],
            data=statuses,
            sorting_reference=config.get_sorted_statuses(),
        )
    )

    skipped = {p.name: e for p, e in project_checker.skipped_modules}
    if skipped:
        tables_to_display.append(
            renderer.get_table(
                title="Skipped modules",
                headers=["Module", "Error", "Rate"],
                data=skipped,
            )
        )

    renderer.display_summary(tables_to_display)  

    renderer.display_project_report(project_report=project_report)

    if settings.no_cache:
        source.cleanup()

    return 0


if __name__ == "__main__":
    with spacing():
        try:
            sys.exit(main())
        except DocstrHealthError as e:
            rich_print(f"[red]{e}[/red]")
            sys.exit(1)
