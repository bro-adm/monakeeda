from abc import ABC, abstractmethod
from enum import Enum
from typing import Tuple, Union


class NumericConstraintOperations(Enum):
    GT = 'gt'
    LT = 'lt'
    LTE = 'lte'
    GTE = 'gte'


class NumericConstraint(ABC):
    @property
    @abstractmethod
    def constraint_info(self) -> Tuple[NumericConstraintOperations, Union[int, float]]:
        pass

    def is_contradiction(self, other) -> bool:
        pass
