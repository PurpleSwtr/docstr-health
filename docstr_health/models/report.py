import ast
import statistics

from ..models.function import PythonFunction


class ModuleReport:
    def __init__(
        self,
        module_status: str,
        inspected_functions: list[PythonFunction],
        docstring_lengths: list[tuple[str, int]] | None = None,
    ) -> None:
        self.module_status: str = module_status
        self.inspected_functions: list[PythonFunction] = inspected_functions
        self.docstring_lengths: list[tuple[str, int]] = docstring_lengths or []

    @property
    def average_docstring_length(self) -> float:
        if not self.docstring_lengths:
            return 0.0
        return float(statistics.mean(length for _, length in self.docstring_lengths))

    @property
    def median_docstring_length(self) -> float:
        if not self.docstring_lengths:
            return 0.0
        return float(statistics.median(length for _, length in self.docstring_lengths))

    @property
    def longest_docstring(self) -> tuple[str, int] | None:
        if not self.docstring_lengths:
            return None
        return max(self.docstring_lengths, key=lambda x: x[1])

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
