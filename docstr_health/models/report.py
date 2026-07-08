import ast

from ..models.function import PythonFunction


class ModuleReport:
    def __init__(
        self, module_status: str, inspected_functions: list[PythonFunction]
    ) -> None:
        self.module_status: str = module_status
        self.inspected_functions: list[PythonFunction] = inspected_functions

    def get_func_type_quantity(self) -> dict:
        res = {"class": 0, "function": 0, "async function": 0}
        for func in self.inspected_functions:
            match func._ast_node:
                case ast.ClassDef():
                    res["class"] += 1
                case ast.AsyncFunctionDef():
                    res["async function"] += 1
                case _:
                    res["function"] += 1
        return res


class ProjectReport: ...
