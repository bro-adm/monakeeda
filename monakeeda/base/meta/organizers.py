from abc import ABC, abstractmethod
from typing import List, Dict, Type

from ..component import Component


class ComponentOrganizer(ABC):
    @abstractmethod
    def order_by_chain_of_responsibility(self, monkey_components: List[Component]) -> Dict[Type[Component], List[Component]]:
        pass

    @abstractmethod
    def order_for_instance_operation(self, monkey_cls, monkey_type_organized_components: Dict[Type[Component], List[Component]]) -> List[Component]:
        pass
