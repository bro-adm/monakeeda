from abc import ABC

from monakeeda.base import BaseDecorator, ExceptionsDict
from monakeeda.consts import NamespacesConsts, FieldConsts
from ..missing.errors import MissingFieldValuesException


class BaseValidatorDecorator(BaseDecorator, ABC):
    __pass_on_errors__ = [MissingFieldValuesException, TypeError]

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        super()._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key].setdefault(FieldConsts.VALIDATORS, []).append(self)

