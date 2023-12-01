from abc import ABC
from typing import List

from .component import Component
from ..exceptions_manager import ExceptionsDict
from ..interfaces import ValuesHandler


class ComponentDecorator(ValuesHandler, ABC):
    def __init__(self):
        self.component: Component = None

    def _extract_relevant_exceptions(self, exceptions: ExceptionsDict) -> List[Exception]:
        return []
