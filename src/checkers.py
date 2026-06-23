from models import PythonModule


class BaseChecker:
    def __init__(self, module: PythonModule) -> None:
        self.module = module


class DocstringChecker(BaseChecker):
    def check(
        self,
    ): ...


class TestCoverageChecker(BaseChecker): ...
