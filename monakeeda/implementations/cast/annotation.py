import inspect
from typing import Generic, T, Any, Union

from monakeeda.base import GenericAnnotation
from ..missing import ValidateMissingFieldsConfigParameter
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from monakeeda.consts import NamespacesConsts
from ..missing.errors import MissingFieldValuesException


class CastingError(ValueError):
    def __init__(self, given_val, wanted_casting_type):
        super(CastingError, self).__init__(
            f'failed casting from type {given_val} to {wanted_casting_type} -> value given is {given_val}')


class Cast(GenericAnnotation, Generic[T]):
    __label__ = 'cast'
    __prior_handler__ = ValidateMissingFieldsConfigParameter
    __pass_on_errors__ = [MissingFieldValuesException]

    def _handle_values(self, model_instance, values, stage):
        cast_to = self._types[0]
        value = values[self._field_key]

        try:
            wanted_value = cast_to(value)
            values[self._field_key] = wanted_value
        except TypeError:
            getattr(model_instance, NamespacesConsts.EXCEPTIONS).append(CastingError(value, cast_to))

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_cast_annotation(self, context)
