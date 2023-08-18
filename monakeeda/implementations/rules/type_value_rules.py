from typing import Union

from monakeeda.base import BaseParameterValueTypeValidationFailedRule, ParameterValueTypeValidationFailedRuleException, \
    Parameter, RuleException


class BasicParameterValueTypeValidationRule(BaseParameterValueTypeValidationFailedRule):
    def validate(self, component: Parameter, monkey_cls) -> Union[RuleException, None]:
        if not isinstance(component.param_val, self.wanted_type):
            return ParameterValueTypeValidationFailedRuleException(component.__key__, component.param_val, self.wanted_type)

