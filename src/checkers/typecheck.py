import ast

from checkers.base import BaseChecker
from core.enums import StatusTypechecking
from models.function import PythonFunction


class TypeChecker(BaseChecker):
    @staticmethod
    def inspect_func_type_checking(func: PythonFunction) -> StatusTypechecking:
        for arg in func._ast_node.args.args:
            if arg.annotation:
                ann_str = ast.unparse(arg.annotation)
            else:
                return StatusTypechecking.ARGS

        if func._ast_node.returns:
            ann_str = ast.unparse(func._ast_node.returns)
        else:
            return StatusTypechecking.RETURN
