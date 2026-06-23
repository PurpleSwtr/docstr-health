import ast
from pathlib import Path


class PythonFunction:
    def __init__(
        self,
        name: str,
        ast_node: ast.FunctionDef | ast.AsyncFunctionDef,
    ):
        self.name = name
        self._ast_node = ast_node

    @property
    def is_dunder(self) -> bool:
        return (
            self.name.startswith("__")
            and self.name.endswith("__")
            and len(self.name) > 4
        )

    @property
    def has_docstring(self) -> bool:
        return ast.get_docstring(self._ast_node) is not None

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
    def functions(
        self,
    ) -> list[PythonFunction]:
        tree = ast.parse(self.file_path.read_text(encoding="utf-8"))
        nodes = [
            node
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]
        return [PythonFunction(name=node.name, ast_node=node) for node in nodes]
