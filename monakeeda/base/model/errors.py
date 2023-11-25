from typing import Dict, Set

from ..exceptions_manager import ExceptionsDict
from ..component import Component


class ScopedComponentsCollisionsException(Exception):
    def __init__(self, labeled_collisions: Dict[str, Set[Component]]):
        self.labeled_collisions = labeled_collisions

    def __str__(self):
        collision_description = f"The following components collided :( -> "

        for label, components in self.labeled_collisions.items():
            collision_description = collision_description + f"\n\t\t Label: {label} -> {[component.representor for component in components]}"

        return collision_description


class MonkeyValuesHandlingException(Exception):
    def __init__(self, monkey_name: str, values: dict, exceptions: ExceptionsDict):
        self.monkey_name = monkey_name
        self.values = values
        self.exceptions = exceptions

    def __str__(self):
        return f"Encountered the following errors when trying to initialize Monkey {self.monkey_name} with values {self.values} -> {self.exceptions}"
