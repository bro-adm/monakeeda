from typing import Dict, Set

from ..exceptions_manager import ExceptionsDict
from ..component import Component


class ScopedLabeledComponentsCollisionsException(Exception):
    def __init__(self, label: str, collisions: Set[str], collided_with=None):
        self.label = label
        self.collisions = collisions
        self.collided_with = collided_with  # by the default they collide with each other and not with a main component

    def __str__(self):
        return f"The following components collided {f'with {self.collided_with} ' if self.collided_with else ''}-> {self.collisions} -> (label={self.label})"


class MonkeyValuesHandlingException(Exception):
    def __init__(self, monkey_name: str, values: dict, exceptions: ExceptionsDict):
        self.monkey_name = monkey_name
        self.values = values
        self.exceptions = exceptions

    def __str__(self):
        return f"Encountered the following errors when trying to initialize Monkey {self.monkey_name} with values {self.values} -> {self.exceptions}"
