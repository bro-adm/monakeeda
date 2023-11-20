from abc import abstractmethod, ABC
from enum import Enum
from typing import ClassVar, Union, TypeVar, Type

from .component import Component
from ..interfaces import RuleException, Rule


class ParameterIdentifier(Enum):
    key = '__key__'
    label = '__label__'


class Parameter(Component, ABC):
    """
    Represent a client set key value concept with the ability like any other component (includes chain of responsibility etc...)
    For now it is only used under the scope of initialization of the Configurable Component.
    """

    __key__: ClassVar[str]  # key for setting value
    __label__: ClassVar[str]  # concept - multiple parameters can be responsible for the same goal (e.g. default & default_factory)

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
