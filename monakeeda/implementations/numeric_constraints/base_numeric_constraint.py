from abc import ABC, abstractmethod
from typing import Generic, T, Tuple, Union

from monakeeda.base import FieldParameter, GenericAnnotation, ExceptionsDict
from .helpers import constraint_collisions_validation
from ..known_builders import ParameterValueTypeValidator, CoreAnnotationsExtractor


class NumericConstraintFieldParameter(FieldParameter, ABC):
    __builders__ = [ParameterValueTypeValidator((int, float)), CoreAnnotationsExtractor(int, float)]

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
        super().is_collision(other)

        key1, val1 = self.constraint
        key2, val2 = other.constraint

        is_valid = constraint_collisions_validation[(key1, key2)](val1, val2) if (key1, key2) in constraint_collisions_validation else constraint_collisions_validation[(key2, key1)](val2, val1)
        return not is_valid


class NumericConstraintAnnotation(GenericAnnotation, Generic[T]):
    __builders__ = [CoreAnnotationsExtractor(int, float)]

    @classmethod
    @property
    def label(cls) -> str:
        return "numeric_constraint"

    @property
    @abstractmethod
    def constraint(self) -> Tuple[str, Union[int, float]]:
        pass

    def is_collision(self, other) -> bool:
        super().is_collision(other)

        key1, val1 = self.constraint
        key2, val2 = other.constraint

        is_valid = constraint_collisions_validation[(key1, key2)](val1, val2) if (key1, key2) in constraint_collisions_validation else constraint_collisions_validation[(key2, key1)](val2, val1)
        return not is_valid

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        super()._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)

        annotation = self.represented_annotations[0]
        annotation.build(monkey_cls, bases, monkey_attrs, exceptions)

        monkey_cls.__type_organized_components__[type(annotation)].append(annotation)
