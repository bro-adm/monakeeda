from typing import Union, List, Any

from monakeeda.base import Rule, Parameter, RuleException


class NotAllowedValueRuleException(RuleException):
    def __init__(self, key: str, value: Any, allowed_values: List[Any]):
        self.key = key
        self.value = value
        self.allowed_values = allowed_values

    def __str__(self):
        return f"{self.key} was provided with value {self.value} which is not in the following allowed values {self.allowed_values}"


class AllowedValuesRule(Rule):
    def __init__(self, allowed_values: List[Any]):
        self.allowed_values = allowed_values

    def validate(self, component: Parameter, monkey_cls) -> Union[RuleException, None]:
        if component.param_val not in self.allowed_values:
            return NotAllowedValueRuleException(component.__key__, component.param_val, self.allowed_values)

        return
