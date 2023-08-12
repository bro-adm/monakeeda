from abc import ABC
from typing import Generic

from base_manager import BaseManager
from .component import TComponent
from .composite_component import BaseComponentComposite


class MainComponent(BaseComponentComposite[TComponent], BaseManager, Generic[TComponent], ABC):
    def _set_cls_landscape(self, monkey_cls, bases, monkey_attrs):
        super()._set_cls_landscape(monkey_cls, bases, monkey_attrs)
        self.run_bases(monkey_cls, bases, monkey_attrs)
