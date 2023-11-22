from typing import Dict, List

from monakeeda.base import Field, MonkeyBuilder, ConfigParameter
from monakeeda.consts import NamespacesConsts, FieldConsts
from monakeeda.helpers import ExceptionsDict


class SomeFieldsDontAcknowledgeKeyException(Exception):
    def __init__(self, key: str, unacknowledged_fields: Dict[str, Field]):
        self.key = key
        self.unacknowledged_fields = unacknowledged_fields

    def __str__(self):
        return f"Wanting to attempt field change of all fields for field setting {self.key}, " \
               f"but not all fields acknowledge this key -> {self.unacknowledged_fields}"


class AllModelFieldsAcknowledgeParameterValidatorBuilder(MonkeyBuilder):
    def __init__(self, key: str):
        self.key = key

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder: ConfigParameter):
        unacknowledged_fields = {}

        for field_key, field_info in getattr(monkey_cls, NamespacesConsts.STRUCT)[NamespacesConsts.FIELDS].items():
            field = field_info[FieldConsts.FIELD]

            if self.key not in [field_parameter.__key__ for field_parameter in field.__parameter_components__]:
                unacknowledged_fields[field_key] = field.__class__

        if unacknowledged_fields:
            exceptions[main_builder._field_key].append(SomeFieldsDontAcknowledgeKeyException(self.key, unacknowledged_fields))
