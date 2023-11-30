from abc import ABC
from typing import ClassVar, TypeVar

from monakeeda.utils import capitalize_words
from .component import Component


class Parameter(Component, ABC):
    """
    Represent a client set key value concept with the ability like any other component (includes chain of responsibility etc...)
    For now it is only used under the scope of initialization of the Configurable Component.
    """

    __key__: ClassVar[str]  # key for setting value

    def __init__(self, param_val):
        super().__init__()
        self.param_val = param_val

    @property
    def representor(self) -> str:
        return capitalize_words(self.__key__)


TParameter = TypeVar('TParameter', bound=Parameter)
