from typing import Generic, T

from monakeeda.base import GenericAnnotation


class ConstError(ValueError):
    def __init__(self, default_val, given_val):
        super(ConstError, self).__init__(
            f'Const field -> its value is {default_val} ... value given = {given_val}')


# TODO: make 'default' be provided via DefaultParameter implementation
class Const(GenericAnnotation, Generic[T]):
    def _act_with_value(self, value, cls, current_field_info):
        const_type = self._types[0]
        if not isinstance(value, const_type):
            raise TypeError(f"field should be of type {const_type}, but got {value} of type {type(value)} instead")

        if 'default' in current_field_info and value != current_field_info['default']:
            raise ConstError(current_field_info['default'], value)

        return value
