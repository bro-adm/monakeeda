from abc import ABC
from typing import Generic

from base_manager import BaseManager
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

