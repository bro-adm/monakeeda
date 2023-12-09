from abc import ABC, abstractmethod
from typing import List, Union

from .component import Component
from ..exceptions_manager import ExceptionsDict
from ..interfaces import ValuesHandler


class ComponentDecorator(ValuesHandler, ABC):
    def __init__(self):
        self.component: Union[Component, 'ComponentDecorator'] = None

    def _extract_relevant_exceptions(self, exceptions: ExceptionsDict) -> List[Exception]:
        return []

    @property
    def actual_component(self) -> Component:
        if isinstance(self.component, ComponentDecorator):
            return self.component.actual_component

        return self.component

    @abstractmethod
    def reset(self):
        pass
