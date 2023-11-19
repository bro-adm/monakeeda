from abc import ABC

from monakeeda.base import BaseDecorator
from monakeeda.consts import NamespacesConsts, FieldConsts
from ..missing.errors import MissingFieldValuesException


class BaseCreatorDecorator(BaseDecorator, ABC):
    __pass_on_errors__ = [MissingFieldValuesException, TypeError]

    def __init__(self, field_key: str):
        self._field_key = field_key

    def build(self, monkey_cls, bases, monkey_attrs):
        # setdefault is in use because this can be set on a none schema parameter
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key].update({FieldConsts.CREATOR: self, FieldConsts.REQUIRED: False})
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.COMPONENTS].append(self)

