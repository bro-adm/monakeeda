from typing import Generic, T, Any

from monakeeda.base import GenericAnnotation, ExceptionsDict
from ..creators import CreateFrom
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor


class CastingError(ValueError):
    def __init__(self, given_val, wanted_casting_type):
        super(CastingError, self).__init__(
            f'failed casting from type {given_val} to {wanted_casting_type} -> value given is {given_val}')


class Cast(GenericAnnotation, Generic[T]):
    __prior_handler__ = CreateFrom

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        cast_to = self._types[0]
        value = values[self._field_key]

        try:
            wanted_value = cast_to(value)
            values[self._field_key] = wanted_value
        except TypeError:
            exceptions[self.scope].append(CastingError(value, cast_to))

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_cast_annotation(self, context)
