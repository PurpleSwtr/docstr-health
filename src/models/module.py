import ast
from pathlib import Path

from core.config import config
from core.exceptions import PythonParseError
from core.logger import logger
from models.function import PythonFunction


class PythonModule:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self._tree: ast.Module | None = None
        self._parse_error: PythonParseError | None = None

    @property
    def tree(self) -> ast.Module | None:
        """Lazy loading ast-tree"""
        if self._tree is None:
            try:
                self._tree = ast.parse(self.file_path.read_text(encoding="utf-8"))
            except Exception as e:
                self._parse_error = PythonParseError(self.file_path, e)
                logger.warning(self.parse_error)
        return self._tree

    @property
    def parse_error(self) -> PythonParseError | None:
        return self._parse_error

    @property
    def functions(self) -> list[PythonFunction]:
        if self.tree:
            nodes = [
                node
                for node in ast.walk(self.tree)
                if isinstance(
                    node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
                )
                and node.name not in config.parameters["excluded_functions"]
            ]
            return [
                PythonFunction(
                    name=node.name, ast_node=node, source_file=self.file_path
                )
                for node in nodes
            ]
        else:
            return []

    @property
    def functions_to_check(self) -> list[PythonFunction]:
        return [
            function
            for function in self.functions
            if not function.is_full_dunder and not function.is_once_dunder
        ]

    def get_module_docstring(self) -> str | None:
        """Returns self docstring of module"""
        if self.tree:
            return ast.get_docstring(self.tree)

    def get_functions_size(self) -> dict[str, int]:
        return {func.name: func.size for func in self.functions}

    def __str__(self):
        return self.file_path.name
