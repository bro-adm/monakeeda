from abc import ABC

from monakeeda.base import BaseDecorator, ExceptionsDict
from monakeeda.consts import NamespacesConsts, FieldConsts


class BaseValidatorDecorator(BaseDecorator, ABC):
    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        super()._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key].setdefault(FieldConsts.VALIDATORS, []).append(self)

