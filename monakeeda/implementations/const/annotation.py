from typing import Generic, T

from monakeeda.base import GenericAnnotation, Stages
from monakeeda.consts import FieldConsts
from .exceptions import ConstError


# TODO: make 'default' be provided via DefaultParameter implementation
class Const(GenericAnnotation, Generic[T]):
    def _act_with_value(self, value, cls, current_field_info, stage):
        const_type = self._types[0]
        if not isinstance(value, const_type):
            raise TypeError(f"field should be of type {const_type}, but got {value} of type {type(value)} instead")

        if stage == Stages.UPDATE:
            curr_val = current_field_info[FieldConsts.VALUE]

            if value != curr_val:
                raise ConstError(curr_val, value)
        else:
            if 'default' in current_field_info and value != current_field_info['default']:
                raise ConstError(current_field_info['default'], value)

        return value
