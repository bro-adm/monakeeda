import inspect
from typing import Callable

from monakeeda.base import Parameter, MonkeyBuilder
from monakeeda.helpers import ExceptionsDict
from .parameter_value_type_validator import ParameterValueTypeValidator


class ParameterCallableValueOverTheAllowedAmountOfArgsException(Exception):
    def __init__(self, parameter: Parameter, allowed_amount_of_args: int, received_amount_of_args: int):
        self.parameter_representor = parameter.representor
        self.received_callable = parameter.param_val
        self.allowed_amount_of_args = allowed_amount_of_args
        self.received_amount_of_args = received_amount_of_args

    def __str__(self):
        return f"{self.parameter_representor} allows to receive a callable with {self.allowed_amount_of_args}, but received one with {self.received_amount_of_args} -> {self.received_callable}"


class ParameterCallableValueValidator(MonkeyBuilder):
    __builders__ = [ParameterValueTypeValidator(Callable)]

    def __init__(self, allowed_amount_of_args: int):
        self.allowed_amount_of_args = allowed_amount_of_args

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder: Parameter):
        callable_signature_parameters = inspect.signature(main_builder.param_val).parameters

        if len(callable_signature_parameters) != self.allowed_amount_of_args:
            exception = ParameterCallableValueOverTheAllowedAmountOfArgsException(main_builder, self.allowed_amount_of_args, len(callable_signature_parameters))
            exceptions[main_builder.scope].append(exception)
