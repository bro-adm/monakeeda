from typing import List, Dict
from monakeeda.helpers import ExceptionsDict


class MonkeyBuildException(Exception):
    def __init__(self, monkey_name: str, exceptions: ExceptionsDict):
        self.monkey_name = monkey_name
        self.exceptions = exceptions

    def __str__(self):
        return f"Encountered the following errors when trying to build Monkey {self.monkey_name}: {self.exceptions}"
