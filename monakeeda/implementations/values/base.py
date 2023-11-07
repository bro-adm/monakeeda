from abc import ABC

from monakeeda.consts import NamespacesConsts, FieldConsts
from monakeeda.base import FieldParameter


class BaseValueFieldParameter(FieldParameter, ABC):
    __label__ = 'value_provider'

    def build(self, monkey_cls, bases, monkey_attrs):
        super(BaseValueFieldParameter, self).build(monkey_cls, bases, monkey_attrs)
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.REQUIRED] = False
