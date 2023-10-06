from typing import Generic, T, Any

from monakeeda.base import GenericAnnotation
from monakeeda.consts import FieldConsts
from ..default import DefaultFactoryFieldParameter
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor


class CastingError(ValueError):
    def __init__(self, given_val, wanted_casting_type):
        super(CastingError, self).__init__(
            f'failed casting from type {given_val} to {wanted_casting_type} -> value given is {given_val}')


class Cast(GenericAnnotation, Generic[T]):
    __label__ = 'cast'
    __prior_handler__ = DefaultFactoryFieldParameter

    def _act_with_value(self, value, cls, current_field_info, stage) -> Any:
        cast_to = self._types[0]
        try:
            wanted_value = cast_to(value)
            current_field_info[FieldConsts.TYPE] = cast_to
            return wanted_value
        except TypeError:
            raise CastingError(value, cast_to)

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_cast_annotation(self, context)
