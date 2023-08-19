from typing import Generic, T

from monakeeda.base import GenericAnnotation
from .exceptions import AbstractFieldFoundError


class Abstract(GenericAnnotation, Generic[T]):

    def _act_with_value(self, value, cls, current_field_info, stage):
        raise AbstractFieldFoundError(self._field_key)
