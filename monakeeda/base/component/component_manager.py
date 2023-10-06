from abc import ABC, abstractmethod
from typing import List

from monakeeda.consts import NamespacesConsts
from .component import Component
from .monkey_builder import MonkeyBuilder


class ComponentManager(MonkeyBuilder, ABC):

    @abstractmethod
    def _components(self, monkey_cls) -> List[Component]:
        pass

    @abstractmethod
    def _set_by_base(self, monkey_cls, base, attrs):
        pass

    @abstractmethod
    def _set_curr_cls(self, monkey_cls, bases, monkey_attrs):
        pass

    def build(self, monkey_cls, bases, monkey_attrs):
        for base in bases:
            self._set_by_base(monkey_cls, base, monkey_attrs)

        self._set_curr_cls(monkey_cls, bases, monkey_attrs)

        components = self._components(monkey_cls)
        monkey_attrs[NamespacesConsts.COMPONENTS].extend(components)
