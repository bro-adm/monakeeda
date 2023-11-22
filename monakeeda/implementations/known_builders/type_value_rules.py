from typing import Union, List

from monakeeda.base import Parameter, MonkeyBuilder
from monakeeda.helpers import ExceptionsDict


class ParameterValueTypeValidationFailedException(Exception):
    def __init__(self, parameter_key, value, wanted_type):
        self.parameter_key = parameter_key
        self.value = value
        self.wanted_type = wanted_type

    def __str__(self):
        return f"{self.parameter_key} -> value {self.value} not of type {self.wanted_type}"


class BasicParameterValueTypeValidatorBuilder(MonkeyBuilder):
    def __init__(self, wanted_ype):
        self.wanted_type = wanted_ype

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder: Parameter):
        if not isinstance(main_builder.param_val, self.wanted_type):
            exceptions[main_builder._field_key].append(ParameterValueTypeValidationFailedException(main_builder.__key__, main_builder.param_val, self.wanted_type))

