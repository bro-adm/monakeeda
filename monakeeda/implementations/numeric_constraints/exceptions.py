from typing import Union

from monakeeda.base import Component


class NumericConstraintFailedException(ValueError):
    def __init__(self, component: Component, constraint_value: Union[int, float], provided_value: Union[int, float]):
        self.component_representor = component.representor
        self.constraint_value = constraint_value
        self.provided_value = provided_value

    def __str__(self):
        return f"{self.component_representor} constraint of {self.constraint_value} not matched -> provided {self.provided_value}"
