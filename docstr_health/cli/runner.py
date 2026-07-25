from ..checkers.project import ProjectChecker
from ..core.config import config

from ..cli.progress_bar import progress_bar


def run_check(project_checker: ProjectChecker):
    quiet = config.parameters.get("ci", False)
    if quiet:
        from collections import deque
        deque(project_checker.docstring_check(), maxlen=0)
        return

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