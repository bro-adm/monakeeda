from abc import ABC, abstractmethod
from typing import List, Dict, Type

from ..component import Component


class ComponentsOrganizer(ABC):
    """
    Post ComponentManagers components discovery, one needs to organize them to run their validations, builds and value handles.

    Validations and builds have a simpler scope and can have the responsibility to generate one another.
    Their run structure is provided via the order_by_chain_of_responsibility.

    Post validations, builds and component generations comes the precise logics available from init and upgrade up to any other operator visitor.
    This is at its final form a simple list which can be hard to set (according to the scope of "concepts" your model supports).
    This list is provided via order_for_instance_operation

    Both methods are run on the scope of the Meta __init__ method therefore making them a one time load operation.
    This means even heavy logics do not effect actual run time (not load time).
    """

    @abstractmethod
    def order_by_chain_of_responsibility(self, monkey_components: List[Component]) -> Dict[Type[Component], List[Component]]:
        pass

    @abstractmethod
    def order_for_instance_operation(self, monkey_cls, monkey_type_organized_components: Dict[Type[Component], List[Component]]) -> Dict[Component, bool]:
        pass
