from abc import abstractmethod, ABC
from typing import ClassVar, Union, TypeVar, Type

from .component import Component
from ..interfaces import RuleException, Rule


class Parameter(Component, ABC):
    __key__: ClassVar[str]

    def __init__(self, param_val):
        self.param_val = param_val


TParameter = TypeVar('TParameter', bound=Type[Parameter])


class ParameterValueTypeValidationFailedRuleException(RuleException):
    def __init__(self, parameter_key, value, wanted_type):
        self.parameter_key = parameter_key
        self.value = value
        self.wanted_type = wanted_type

    def __str__(self):
        return f"{self.parameter_key} -> value {self.value} not of type {self.wanted_type}"


class BaseParameterValueTypeValidationFailedRule(Rule, ABC):
    def __init__(self, wanted_type):
        self.wanted_type = wanted_type

    @abstractmethod
    def validate(self, component: Parameter, monkey_cls) -> Union[RuleException, None]:
        pass
