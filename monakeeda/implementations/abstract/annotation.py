from typing import Generic, T

from monakeeda.base import GenericAnnotation, Config
from .exceptions import AbstractFieldFoundError


class Abstract(GenericAnnotation, Generic[T]):
    __label__ = 'abstract'
    __prior_handler__ = Config

    def handle_values(self, model_instance, values, stage) -> dict:
        raise AbstractFieldFoundError(self._field_key)

    def _act_with_value(self, value, cls, current_field_info, stage):
        pass
