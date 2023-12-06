from abc import ABC

from monakeeda.base import BaseDecorator, ExceptionsDict
from monakeeda.consts import NamespacesConsts, FieldConsts
from .consts import KnownLabels
from .validate_missing_fields_config_parameter import ValidateMissingFieldsConfigParameter


class BaseCreatorDecorator(BaseDecorator, ABC):
    __prior_handler__ = ValidateMissingFieldsConfigParameter.label

    @classmethod
    @property
    def label(cls) -> str:
        return KnownLabels.EXISTENCE_MANAGER

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        super()._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.REQUIRED] = False
