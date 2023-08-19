from abc import ABC
from typing import Generic, List

from .base_manager import BaseManager
from .component import TComponent
from .composite_component import BaseComponentComposite


class MainComponent(BaseComponentComposite[TComponent], BaseManager, Generic[TComponent], ABC):
    """
    Meant for concept managers that usually if not always need to also run bases setups.
    Beware of instance variables!!!

    Operation order:
        - run_bases
        - components
        - build
        - init

    No validations are required for Main Components bases+cls setup ->
    inner components should not run their landscapes prior to validators !!!
    """

    pass


class MainComponentInitComposite(BaseComponentComposite[MainComponent]):
    def __init__(self, components: List[MainComponent]):
        self._init_components = components

    def _components(self, monkey_cls) -> List[MainComponent]:
        return self._init_components

    def run_bases(self, monkey_cls, bases, monkey_attrs):
        for component in self._components(monkey_cls):
            component.run_bases(monkey_cls, bases, monkey_attrs)
