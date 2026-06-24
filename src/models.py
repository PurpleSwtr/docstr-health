import ast
from pathlib import Path

from core.config import config


class PythonFunction:
    def __init__(
        self,
        name: str,
        ast_node: ast.FunctionDef | ast.AsyncFunctionDef,
        source_file: Path | None = None,
    ):
        self.name = name
        self._ast_node = ast_node
        self._source_file = source_file

    @property
    def is_full_dunder(self) -> bool:
        return (
            self.name.startswith("__")
            and self.name.endswith("__")
            and len(self.name) > 4
        )

    @property
    def is_once_dunder(self) -> bool:
        return self.name.startswith("_") and len(self.name) > 1

    @property
    def size(self) -> int:
        if self._ast_node.end_lineno:
            return self._ast_node.end_lineno - self._ast_node.lineno + 1
        return 0

    @property
    def has_docstring(self) -> bool:
        return ast.get_docstring(self._ast_node) is not None

    def get_docstring(self) -> str | None:
        return ast.get_docstring(self._ast_node)

    def is_decorator_applied(self, decorator_name: str) -> bool:
        return self._has_decorator(decorator_name=decorator_name)

    def _has_decorator(self, decorator_name: str) -> bool:
        for decorator in self._ast_node.decorator_list:
            if isinstance(decorator, ast.Name) and decorator.id == decorator_name:
                return True
            if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name):
                if decorator.func.id == decorator_name:
                    return True
        return False


class PythonModule:
    def __init__(self, file_path: Path):
        self.file_path = file_path

    @property
    def functions(self) -> list[PythonFunction]:
        tree = ast.parse(self.file_path.read_text(encoding="utf-8"))
        nodes = [
            node
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name not in config.parameters["excluded_functions"]
        ]
        return [
            PythonFunction(name=node.name, ast_node=node, source_file=self.file_path)
            for node in nodes
        ]

    @property
    def functions_to_check(self) -> list[PythonFunction]:
        return [
            function
            for function in self.functions
            if not function.is_full_dunder and not function.is_once_dunder
        ]

    def get_functions_size(self) -> dict[str, int]:
        return {func.name: func.size for func in self.functions}

    def __str__(self):
        return self.file_path.name
