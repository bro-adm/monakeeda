from ..exceptions_manager import ExceptionsDict


class MonkeyValuesHandlingException(Exception):
    def __init__(self, monkey_name: str, values: dict, exceptions: ExceptionsDict):
        self.monkey_name = monkey_name
        self.values = values
        self.exceptions = exceptions

    def __str__(self):
        return f"Encountered the following errors when trying to initialize Monkey {self.monkey_name} with values {self.values} -> {self.exceptions}"
