from abc import ABC

from monakeeda.consts import NamespacesConsts, FieldConsts
from monakeeda.base import FieldParameter


class BaseDefaultFieldParameter(FieldParameter, ABC):
    __label__ = 'default_provider'

    def build(self, monkey_cls, bases, monkey_attrs):
        super(BaseDefaultFieldParameter, self).build(monkey_cls, bases, monkey_attrs)
        monkey_cls.__map__[NamespacesConsts.FIELDS][self._field_key][FieldConsts.REQUIRED] = False
