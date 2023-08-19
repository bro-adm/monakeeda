from typing import Generic, T

from monakeeda.base import GenericAnnotation
from monakeeda.consts import FieldConsts


class CastingError(ValueError):
    def __init__(self, given_val, wanted_casting_type):
        super(CastingError, self).__init__(
            f'failed casting from type {given_val} to {wanted_casting_type} -> value given is {given_val}')


class Cast(GenericAnnotation, Generic[T]):
    def _act_with_value(self, value, cls, current_field_info, stage):
        cast_to = self._types[0]
        try:
            wanted_value = cast_to(value)
            current_field_info[FieldConsts.TYPE] = cast_to
            return wanted_value
        except TypeError:
            raise CastingError(value, cast_to)
