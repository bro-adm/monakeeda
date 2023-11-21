from abc import ABC
from typing import List

from monakeeda.base import FieldParameter
from monakeeda.consts import NamespacesConsts, FieldConsts


class BaseValueFieldParameter(FieldParameter, ABC):
    __label__ = 'value_provider'

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: List[Exception], main_builder):
        super(BaseValueFieldParameter, self)._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.REQUIRED] = False
