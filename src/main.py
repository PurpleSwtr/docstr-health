import sys
from contextlib import contextmanager

from rich import print as rich_print
from rich.columns import Columns

from checkers.project import ProjectChecker
from cli.cli import RichOutput
from cli.parser import get_parser
from cli.progress_bar import progress_bar
from core.config import config
from core.settings import AppSettings
from sources.git_repo import GitRepositorySource
from sources.local import LocalSource


@contextmanager
def spacing():
    print()
    yield


def main():
    parser = get_parser()
    args = parser.parse_args()
    settings = AppSettings.from_args(args)

    if args.repo_url:
        source = GitRepositorySource(args.repo_url)
    else:
        source = LocalSource(args.project_path)

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

    statuses = project_checker._get_statuses_stat()

    general_stat_data = project_checker.get_quantity_of_func_type()
    if args.doc_modules:
        general_stat_data["modules"] = project_checker._get_count_modules()
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

    # python_functions = map(lambda x: get_functions(x), python_files)

    # for module in modules:
    #     checker = TypeChecker(module)
    #     for func in module.functions_to_check:
    #         checker.inspect_func_type_checking(func=func)
    # print(f"{func.name} - {func.size}")

    # print(modules[0].get_functions_size())
    # print(
    #     f"Найдено: {len(all_functions_checked)} функций: {', '.join(func.name for func in all_functions_checked)}"
    # )
    # print(
    #     f"Докстринги написаны для: {sum(func.has_docstring for func in all_functions_checked)}/{len(all_functions_checked)}"
    # )


if __name__ == "__main__":
    with spacing():
        sys.exit(main())
