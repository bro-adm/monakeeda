from abc import ABC
from typing import ClassVar, TypeVar, Type, List

from .monkey_builder import MonkeyBuilder
from .rules import Rules, NoComponentDependenciesFailedRule
from .rules_validator import RulesValidator
from .values_handler import ValuesHandler

all_components = []


class Component(RulesValidator, MonkeyBuilder, ValuesHandler, ABC):
    __label__: ClassVar[str]
    __next_handler__: ClassVar[Type['Component']]
    __rules__: ClassVar[Rules] = Rules([NoComponentDependenciesFailedRule()])
    __dependencies__: ClassVar[List[Type['Component']]] = []

    def __init_subclass__(cls):
        if all_components:
            position = all_components.index(str(cls.__next_handler__))
            all_components.insert(position, str(cls))
        else:
            all_components.append(str(cls))

    def __str__(self):
        return f"{self.__label__} component"


TComponent = TypeVar('TComponent', bound=Type[Component])
