from checkers.project import ProjectChecker
from cli.cli import RichOutput
from cli.parser import get_parser
from core.config import config

if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()

    target_dir = args.project_path
    excluded = config.excluded

    project_checker = ProjectChecker(target_dir=target_dir, excluded=excluded)

    project_checker.docstring_check()

    statuses = project_checker._get_statuses_stat()
    renderer = RichOutput()
    renderer.display_table(
        title="Number of modules of each status",
        headers=["Module status", "Quantity"],
        data=statuses,
    )

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
