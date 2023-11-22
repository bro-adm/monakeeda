import inspect
from typing import Callable, List

from monakeeda.base import Parameter, MonkeyBuilder
from monakeeda.helpers import ExceptionsDict
from .type_value_rules import BasicParameterValueTypeValidatorBuilder


class CallableOverTheAllowedAmountOfParametersException(Exception):
    def __init__(self, parameter_key, amount_of_parameters_allowed, amount_of_parameters_received):
        self.parameter_key = parameter_key
        self.amount_of_parameters_allowed = amount_of_parameters_allowed
        self.amount_of_parameters_received = amount_of_parameters_received

    def __str__(self):
        return f"{self.parameter_key} method does not allow more than {self.amount_of_parameters_allowed} parameters -> amount asked for {self.amount_of_parameters_received}"


class CallableParameterSignatureValidatorBuilder(MonkeyBuilder):
    __builders__ = [BasicParameterValueTypeValidatorBuilder(Callable)]

    def __init__(self, amount_of_parameters_allowed: int):
        self.amount_of_parameters_allowed = amount_of_parameters_allowed

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder: Parameter):
        callable_signature_parameters = inspect.signature(main_builder.param_val).parameters

        if len(callable_signature_parameters) != self.amount_of_parameters_allowed:
            exceptions[main_builder._field_key].append(CallableOverTheAllowedAmountOfParametersException(main_builder.__key__, self.amount_of_parameters_allowed, len(callable_signature_parameters)))
