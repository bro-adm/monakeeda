import inspect
from typing import Callable, List

from monakeeda.base import Parameter
from .type_value_rules import BasicParameterValueTypeValidatorBuilder


class CallableOverTheAllowedAmountOfParametersException(Exception):
    def __init__(self, parameter_key, amount_of_parameters_allowed, amount_of_parameters_received):
        self.parameter_key = parameter_key
        self.amount_of_parameters_allowed = amount_of_parameters_allowed
        self.amount_of_parameters_received = amount_of_parameters_received

    def __str__(self):
        return f"{self.parameter_key} method does not allow more than {self.amount_of_parameters_allowed} parameters -> amount asked for {self.amount_of_parameters_received}"


class CallableParameterSignatureValidatorBuilder(BasicParameterValueTypeValidatorBuilder):
    def __init__(self, amount_of_parameters_allowed: int):
        super().__init__(Callable)
        self.amount_of_parameters_allowed = amount_of_parameters_allowed

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: List[Exception], main_builder: Parameter):
        super_validation_result = super()._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)

        if super_validation_result:
            return super_validation_result

        if not super_validation_result:
            callable_signature_parameters = inspect.signature(main_builder.param_val).parameters

            if len(callable_signature_parameters) != self.amount_of_parameters_allowed:
                exceptions.append(CallableOverTheAllowedAmountOfParametersException(main_builder.__key__, self.amount_of_parameters_allowed, len(callable_signature_parameters)))
