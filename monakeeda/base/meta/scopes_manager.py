from abc import ABC, abstractmethod

from ..exceptions_manager import ExceptionsDict
from ..interfaces import MonkeyBuilder
from ..scope import ScopeDict


class ScopesManager(MonkeyBuilder, ABC):
    @abstractmethod
    def _manage_label_duplications(self, main_scope: str, labeled_components: ScopeDict, exceptions: ExceptionsDict):
        pass

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        for scope, scope_info in monkey_cls.scopes.items():
            self._manage_label_duplications(scope, scope_info, exceptions)
