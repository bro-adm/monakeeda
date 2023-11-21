from abc import ABC
from enum import Enum
from typing import ClassVar, TypeVar, Type

from .component import Component


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
