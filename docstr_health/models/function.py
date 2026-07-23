import ast


class PythonFunction:
    def __init__(self, name: str, ast_node, source_file=None):
        self._source_file = source_file
        self.node_type: str = type(ast_node).__name__
        self.name: str = self._set_name(name)
        self.lineno: int = ast_node.lineno
        self.end_lineno: int | None = ast_node.end_lineno
        self._docstring: str | None = ast.get_docstring(ast_node)
        self._decorator_names: list[str] = self._extract_decorators(ast_node)

    def _set_name(self, name: str) -> str:
        match self.node_type:
            case "ClassDef":
                return f"{name} (class)"
            case "AsyncFunctionDef":
                return f"{name} (async)"
            case _:
                return name

    @staticmethod
    def _extract_decorators(ast_node) -> list[str]:
        names = []
        for dec in ast_node.decorator_list:
            if isinstance(dec, ast.Name):
                names.append(dec.id)
            elif isinstance(dec, ast.Call) and isinstance(dec.func, ast.Name):
                names.append(dec.func.id)
        return names

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
        if self.end_lineno:
            return self.end_lineno - self.lineno
        return 0

    @property
    def has_docstring(self) -> bool:
        return self._docstring is not None

    def get_docstring(self) -> str | None:
        return self._docstring

    def is_decorator_applied(self, decorator_name: str) -> bool:
        return decorator_name in self._decorator_names
