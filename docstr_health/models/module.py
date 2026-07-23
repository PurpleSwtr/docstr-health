import ast
from pathlib import Path

from ..core.config import config
from ..core.exceptions import PythonParseError
from ..core.logger import logger
from ..models.function import PythonFunction

_UNSET = object()


class PythonModule:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self._tree: ast.Module | None = None
        self._functions: list[PythonFunction] | None = None
        self._functions_to_check: list[PythonFunction] | None = None
        self._module_docstring = _UNSET

    @property
    def tree(self) -> ast.Module | None:
        """Lazy loading ast-tree"""
        if self._tree is None:
            try:
                self._tree = ast.parse(
                    self.file_path.read_text(encoding="utf-8"),
                    filename=str(self.file_path),
                    type_comments=False,
                )
            except Exception as e:
                logger.debug(e)
                raise PythonParseError(self.file_path, e)
        return self._tree

    def release_tree(self):
        self._tree = None

    @property
    def functions(self) -> list[PythonFunction]:
        if self._functions is None:
            if self.tree:
                nodes = [
                    node
                    for node in ast.walk(self.tree)
                    if isinstance(
                        node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
                    )
                    and node.name not in config.parameters["excluded_functions"]
                ]
                self._functions = [
                    PythonFunction(
                        name=node.name, ast_node=node, source_file=self.file_path
                    )
                    for node in nodes
                ]
            else:
                self._functions = []
        return self._functions

    @property
    def functions_to_check(self) -> list[PythonFunction]:
        if self._functions_to_check is None:
            self._functions_to_check = [
                f
                for f in self.functions
                if not f.is_full_dunder and not f.is_once_dunder
            ]
        return self._functions_to_check

    def get_module_docstring(self) -> str | object | None:
        if self._module_docstring is _UNSET:
            self._module_docstring = ast.get_docstring(self.tree) if self.tree else None
        return self._module_docstring

    def get_functions_size(self) -> dict[str, int]:
        return {func.name: func.size for func in self.functions}

    def __str__(self):
        return self.file_path.name
