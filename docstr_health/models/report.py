import ast

from ..models.function import PythonFunction


class ModuleReport:
    def __init__(
        self, module_status: str, inspected_functions: list[PythonFunction]
    ) -> None:
        self.module_status: str = module_status
        self._func_names: list[str] = [f.name for f in inspected_functions]
        self._func_types: dict[str, int] = self._count_types(inspected_functions)

    def _count_types(self, functions: list[PythonFunction]) -> dict[str, int]:
        res = {"class": 0, "function": 0, "async function": 0}
        for func in functions:
            match func._ast_node:
                case ast.ClassDef():
                    res["class"] += 1
                case ast.AsyncFunctionDef():
                    res["async function"] += 1
                case _:
                    res["function"] += 1
        return res

    @property
    def inspected_functions(self):
        return self._func_names

    def get_func_type_quantity(self) -> dict:
        return self._func_types


class ProjectReport: ...
