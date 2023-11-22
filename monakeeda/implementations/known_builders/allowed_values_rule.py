from typing import List, Any

from monakeeda.base import Parameter, MonkeyBuilder
from monakeeda.helpers import ExceptionsDict


class ParameterProvidedValueNotAllowedException(Exception):
    def __init__(self, key: str, value: Any, allowed_values: List[Any]):
        self.key = key
        self.value = value
        self.allowed_values = allowed_values

    def __str__(self):
        return f"{self.key} was provided with value {self.value} which is not in the following allowed values {self.allowed_values}"


class ParameterAllowedValuesValidatorBuilder(MonkeyBuilder):
    def __init__(self, allowed_values: List[Any]):
        self.allowed_values = allowed_values

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder: Parameter):
        if main_builder.param_val not in self.allowed_values:
            exceptions[main_builder._field_key].append(ParameterProvidedValueNotAllowedException(main_builder.__key__, main_builder.param_val, self.allowed_values))

