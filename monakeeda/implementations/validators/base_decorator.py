from abc import ABC
from typing import List

from monakeeda.base import BaseDecorator
from monakeeda.consts import NamespacesConsts, FieldConsts
from ..missing.errors import MissingFieldValuesException


class BaseValidatorDecorator(BaseDecorator, ABC):
    __label__ = 'validators'
    __pass_on_errors__ = [MissingFieldValuesException, TypeError]

    def __init__(self, field_key: str):
        self._field_key = field_key

    def build(self, monkey_cls, bases, monkey_attrs):
        # setdefault is in use because this can be set on a none schema parameter
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS].setdefault(self._field_key, {}).setdefault(FieldConsts.VALIDATORS, []).append(self)
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.COMPONENTS].append(self)

