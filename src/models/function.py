import ast
from pathlib import Path


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
            return self._ast_node.end_lineno - self._ast_node.lineno
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
