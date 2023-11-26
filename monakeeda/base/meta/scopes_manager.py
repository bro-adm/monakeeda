from abc import ABC, abstractmethod
from typing import List

from ..component import Component
from ..exceptions_manager import ExceptionsDict
from ..interfaces import MonkeyBuilder


class ScopesManager(MonkeyBuilder, ABC):
    @abstractmethod
    def _manage_label_duplications(self, scope: str, scoped_components: List[Component], exceptions: ExceptionsDict):
        pass

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        for scope, scope_info in monkey_cls.scopes.items():
            self._manage_label_duplications(scope, scope_info, exceptions)
