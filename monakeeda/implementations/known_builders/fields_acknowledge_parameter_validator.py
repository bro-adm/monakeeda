from abc import ABC
from typing import Dict

from monakeeda.base import MonkeyBuilder, ConfigParameter
from monakeeda.consts import NamespacesConsts, FieldConsts
from monakeeda.helpers import ExceptionsDict


class FieldsDontAcknowledgeParameterKeyException(Exception):
    def __init__(self, component: str, parameter_key: str, unacknowledged_fields: Dict[str, str]):
        self.component = component
        self.parameter_key = parameter_key
        self.unacknowledged_fields = unacknowledged_fields

    def __str__(self):
        return f"{self.component} dependent on fields to acknowledge key {self.parameter_key} but not all do :( -> {self.unacknowledged_fields}"


class BaseFieldsAcknowledgeParameterValidator(MonkeyBuilder, ABC):
    def __init__(self, parameter_key: str):
        self.parameter_key = parameter_key

    def _map_unacknowledged_fields(self, monkey_cls, bases, monkey_attrs, main_builder) -> Dict[str, str]:
        unacknowledged_fields = {}

        for field_key, field_info in monkey_cls.struct[NamespacesConsts.FIELDS].items():
            field = field_info[FieldConsts.FIELD]

            if self.parameter_key not in [field_parameter.__key__ for field_parameter in field.__parameter_components__]:
                unacknowledged_fields[field_key] = field.__class__.__name__

        return unacknowledged_fields


class AllFieldsAcknowledgeParameterValidator(BaseFieldsAcknowledgeParameterValidator):
    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder: ConfigParameter):
        unacknowledged_fields = self._map_unacknowledged_fields(monkey_cls, bases, monkey_attrs, main_builder)

        if unacknowledged_fields:
            exception = FieldsDontAcknowledgeParameterKeyException(main_builder.__key__, self.parameter_key, unacknowledged_fields)
            exceptions[main_builder._config_cls_name].append(exception)
