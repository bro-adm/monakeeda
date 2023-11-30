from abc import ABC, abstractmethod
from typing import Generic, T, Tuple, Union

from monakeeda.base import FieldParameter, GenericAnnotation, ExceptionsDict
from .helpers import constraint_collisions_validation
from ..known_builders import ParameterValueTypeValidator, CoreAnnotationsExtractor


class NumericConstraintFieldParameter(FieldParameter, ABC):
    # __builders__ = [ParameterValueTypeValidator((int, float)), CoreAnnotationsExtractor(int, float)]

    @classmethod
    @property
    def label(cls) -> str:
        return "numeric_constraint"

    @property
    def representor(self) -> str:
        return self.__key__

    @property
    def constraint(self) -> Tuple[str, Union[int, float]]:
        return self.representor, self.param_val

    def is_collision(self, other) -> bool:
        if super().is_collision(other):

            key1, val1 = self.constraint
            key2, val2 = other.constraint

            is_valid = constraint_collisions_validation[(key1, key2)](val1, val2) if (key1, key2) in constraint_collisions_validation else constraint_collisions_validation[(key2, key1)](val2, val1)
            return not is_valid

        return False

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        if not self.is_managed:
            exceptions[self._field_key].append(Exception(f"{self.representor} must be set along a int or float"))


class NumericConstraintAnnotation(GenericAnnotation, Generic[T]):
    @classmethod
    @property
    def label(cls) -> str:
        return "numeric_constraint"

    @property
    def represented_types(self) -> Union[Tuple[type], type]:
        return self

    @property
    @abstractmethod
    def constraint(self) -> Tuple[str, Union[int, float]]:
        pass

    def is_collision(self, other) -> bool:
        if super().is_collision(other):  # non-managed Annotations combo or Annotation+FieldParameter combo of the same label and same manager
            key1, val1 = self.constraint
            key2, val2 = other.constraint

            is_valid = constraint_collisions_validation[(key1, key2)](val1, val2) if (key1, key2) in constraint_collisions_validation else constraint_collisions_validation[(key2, key1)](val2, val1)
            return not is_valid

        return False

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        super()._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)

        if not self.is_managed:
            exceptions[self._field_key].append(Exception(f"{self.representor} must be set along a int or float"))
