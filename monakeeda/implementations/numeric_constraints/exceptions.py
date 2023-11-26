from typing import Union


class NumericConstraintFailedException(ValueError):
    def __init__(self, constraint: str, provided_value: Union[int, float]):
        self.constraint = constraint
        self.provided_value = provided_value

    def __str__(self):
        return f"{self.constraint} constraint not matched -> provided {self.provided_value}"
