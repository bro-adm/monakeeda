from abc import ABC, abstractmethod
from typing import List, Union, Generic, Optional

from .component import Component, TComponent
from ..exceptions_manager import ExceptionsDict
from ..interfaces import ValuesHandler, MonkeyBuilder


class ComponentDecorator(ValuesHandler, MonkeyBuilder, ABC, Generic[TComponent]):
    def __init__(self, decorating_component: TComponent):
        self._decorating_component = decorating_component
        self.decorated: Union[Component, 'ComponentDecorator'] = None
        self.component_actuator: Component = None

    def _extract_relevant_exceptions(self, exceptions: ExceptionsDict) -> List[Exception]:
        return []

    @property
    def component(self) -> Component:
        if isinstance(self.decorated, ComponentDecorator):
            return self.decorated.component

        return self.decorated

    @property
    def direct_decorator_component(self) -> Component:
        if isinstance(self.decorated, ComponentDecorator):
            return self.decorated.direct_decorator_component

        return self._decorating_component

    @abstractmethod
    def reset(self):
        pass
