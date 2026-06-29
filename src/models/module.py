import ast
from pathlib import Path

from core.config import config
from models.function import PythonFunction


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
