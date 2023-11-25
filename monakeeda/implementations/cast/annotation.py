from typing import Generic, T, Any

from monakeeda.base import GenericAnnotation, ExceptionsDict
from ..creators import CreateFrom
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor


class CastingError(ValueError):
    def __init__(self, given_val, wanted_casting_type):
        self.given_val = given_val
        self.wanted_casting_type = wanted_casting_type

    def __str__(self):
        return f'failed casting from {self.given_val} of {type(self.given_val)} to {self.wanted_casting_type}'


class Cast(GenericAnnotation, Generic[T]):
    __prior_handler__ = CreateFrom

    @classmethod
    @property
    def label(cls) -> str:
        return "type_management"

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        cast_to = self._types[0]
        value = values[self.scope]

        try:
            wanted_value = cast_to(value)
            values[self.scope] = wanted_value
        except TypeError:
            exceptions[self.scope].append(CastingError(value, cast_to))

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_cast_annotation(self, context)
