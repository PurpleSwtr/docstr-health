from rich import print
from rich.columns import Columns

from checkers.project import ProjectChecker
from cli.cli import RichOutput
from cli.parser import get_parser
from core.config import config
from sources.git_repo import GitRepositorySource
from sources.local import LocalSource


def main():
    parser = get_parser()
    args = parser.parse_args()

    source = None
    excluded = config.excluded

    if args.repo_url:
        source = GitRepositorySource(args.repo_url)
    else:
        source = LocalSource(args.project_path)

    project_checker = ProjectChecker(source=source, excluded=excluded, args=args)

    project_checker.docstring_check()

    renderer = RichOutput()

    statuses = project_checker._get_statuses_stat()

    general_stat_data = project_checker.get_quantity_of_func_type()
    if args.doc_modules:
        general_stat_data["modules"] = project_checker._get_count_modules()
    general_stat_data["total"] = sum(general_stat_data.values())

    table1 = renderer.get_table(
        title="General statistics",
        headers=["Metric", "Value"],
        data=general_stat_data,
        sorting_reference=config.get_sorted_general_stat(),
        last_line_separator=True,
    )
    table2 = renderer.get_table(
        title="Number of modules of each status",
        headers=["Module status", "Quantity"],
        data=statuses,
        sorting_reference=config.get_sorted_statuses(),
    )
    print(Columns([table1, table2]))
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
    main()
