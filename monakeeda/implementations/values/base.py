from abc import ABC

from monakeeda.base import FieldParameter, ExceptionsDict
from monakeeda.consts import NamespacesConsts, FieldConsts


class BaseValueFieldParameter(FieldParameter, ABC):
    @classmethod
    @property
    def label(cls) -> str:
        return "value_provider"

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        super(BaseValueFieldParameter, self)._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.REQUIRED] = False
