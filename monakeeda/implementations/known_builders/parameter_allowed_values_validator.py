from typing import List, Any

from monakeeda.base import Parameter, MonkeyBuilder
from monakeeda.helpers import ExceptionsDict


class ParameterProvidedValueNotInAllowedValuesException(Exception):
    def __init__(self, parameter: Parameter, allowed_values: List[Any]):
        self.parameter_representor = parameter.representor
        self.provided_value = parameter.param_val
        self.allowed_values = allowed_values

    def __str__(self):
        return f"{self.parameter_representor} parameter was provided with value {self.provided_value} which is not in the following allowed values {self.allowed_values}"


class ParameterAllowedValuesValidator(MonkeyBuilder):
    def __init__(self, allowed_values: List[Any]):
        self.allowed_values = allowed_values

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder: Parameter):
        if main_builder.param_val not in self.allowed_values:
            exception = ParameterProvidedValueNotInAllowedValuesException(main_builder, self.allowed_values)
            exceptions[main_builder._field_key].append(exception)
