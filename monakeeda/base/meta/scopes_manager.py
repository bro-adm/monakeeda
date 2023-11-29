from abc import ABC, abstractmethod
from typing import List

from ..component import Component
from ..exceptions_manager import ExceptionsDict
from ..interfaces import MonkeyBuilder
from ..scope import ScopesDict, extract_main_scope, extract_all_components_of_main_scope


class ScopesManager(MonkeyBuilder, ABC):
    @abstractmethod
    def _manage_label_duplications(self, main_scope: str, scoped_components: ScopesDict, exceptions: ExceptionsDict):
        pass

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        processed_scopes = []

        for scope, scope_info in monkey_cls.scopes.items():
            if scope not in processed_scopes:
                main_scope = extract_main_scope(scope)
                matching_scopes, all_components = extract_all_components_of_main_scope(monkey_cls.scopes, main_scope)

                scope_info = {relevant_scope: monkey_cls.scopes[relevant_scope] for relevant_scope in matching_scopes}

                self._manage_label_duplications(scope, scope_info, exceptions)
                processed_scopes.extend(matching_scopes)

