import inspect
from typing import Callable

from monakeeda.base import Parameter, RuleException
from .type_value_rules import BasicParameterValueTypeValidationRule


class CallableOverTheAllowedAmountOfParametersRuleException(RuleException):
    def __init__(self, parameter_key, amount_of_parameters_allowed, amount_of_parameters_received):
        self.parameter_key = parameter_key
        self.amount_of_parameters_allowed = amount_of_parameters_allowed
        self.amount_of_parameters_received = amount_of_parameters_received

    def __str__(self):
        return f"{self.parameter_key} method does not allow more than {self.amount_of_parameters_allowed} parameters -> amount asked for {self.amount_of_parameters_received}"


class CallableParameterSignatureValidationRule(BasicParameterValueTypeValidationRule):
    def __init__(self, amount_of_parameters_allowed: int):
        super(CallableParameterSignatureValidationRule, self).__init__(Callable)
        self.amount_of_parameters_allowed = amount_of_parameters_allowed

    def validate(self, component: Parameter, monkey_cls):
        super_validation_result = super(CallableParameterSignatureValidationRule, self).validate(component, monkey_cls)

        if super_validation_result:
            return super_validation_result

        if not super_validation_result:
            callable_signature_parameters = inspect.signature(component.param_val).parameters

            if len(callable_signature_parameters) != self.amount_of_parameters_allowed:
                return CallableOverTheAllowedAmountOfParametersRuleException(component.__key__,
                                                                             self.amount_of_parameters_allowed,
                                                                             len(callable_signature_parameters))
