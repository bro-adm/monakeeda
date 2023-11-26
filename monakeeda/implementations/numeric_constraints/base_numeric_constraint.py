from abc import ABC

from monakeeda.base import FieldParameter
from ..known_builders import ParameterValueTypeValidator, CoreAnnotationsExtractor
from .helpers import constraint_collisions_validation


class NumericConstraintFieldParameter(FieldParameter, ABC):
    __builders__ = [ParameterValueTypeValidator((int, float)), CoreAnnotationsExtractor(int, float)]

    @classmethod
    @property
    def label(cls) -> str:
        return "numeric_constraint"

    @property
    def representor(self) -> str:
        return self.__key__

    def is_collision(self, other) -> bool:
        super().is_collision(other)

        key1, val1 = self.__key__, self.param_val
        key2, val2 = other.__key__, other.param_val

        is_valid = constraint_collisions_validation[(key1, key2)](val1, val2) if (key1, key2) in constraint_collisions_validation else constraint_collisions_validation[(key2, key1)](val2, val1)
        return not is_valid
