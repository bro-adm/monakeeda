from abc import ABC
from typing import Generic

from base_manager import BaseManager
from .component import TComponent
from .composite_component import BaseComponentComposite


class MainComponent(BaseComponentComposite[TComponent], BaseManager, Generic[TComponent], ABC):
    pass
