from typing import Union, Dict

from monakeeda.base import Rule, ConfigParameter, RuleException, Field
from monakeeda.consts import NamespacesConsts, FieldConsts


class AllClassAttrsFieldsDontAcknowledgeKeyRuleException(RuleException):
    def __init__(self, key: str, unacknowledged_fields: Dict[str, Field]):
        self.key = key
        self.unacknowledged_fields = unacknowledged_fields

    def __str__(self):
        return f"Wanting to attempt field change of all fields for field setting {self.key}, " \
               f"but not all fields acknowledge this key -> {self.unacknowledged_fields}"


class AllModelFieldsAcknowledgeParameterRule(Rule):
    def __init__(self, key: str):
        self.key = key

    def validate(self, component: ConfigParameter, monkey_cls) -> Union[RuleException, None]:
        unacknowledged_fields = {}

        for field_key, field_info in monkey_cls.__map__[NamespacesConsts.FIELDS].items():
            field = field_info[FieldConsts.FIELD]

            if self.key not in [field_parameter.__key__ for field_parameter in field.__parameters_components__]:
                unacknowledged_fields[field_key] = field.__class__

        if unacknowledged_fields:
            return AllClassAttrsFieldsDontAcknowledgeKeyRuleException(self.key, unacknowledged_fields)
