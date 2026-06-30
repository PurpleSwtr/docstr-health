class GitNotInstalledError(Exception):
    def __init__(
        self,
        message="Git are not installed on this machine. Please, install git before running this command.",
    ):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"
