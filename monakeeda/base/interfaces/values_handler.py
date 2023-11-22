from abc import ABC, abstractmethod
from typing import ClassVar, List, Type

from monakeeda.utils import get_items_from_list
from ..exceptions_manager import ExceptionsDict


class ValuesHandler(ABC):
    __pass_on_errors__: ClassVar[List[Type[Exception]]] = []

    @abstractmethod
    def _extract_relevant_exceptions(self, exceptions: ExceptionsDict) -> List[Exception]:
        pass

    def handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        relevant_exceptions = self._extract_relevant_exceptions(exceptions)
        relevant_exception_types = {type(e) for e in relevant_exceptions}
        existing_dependent_errors = get_items_from_list(self.__pass_on_errors__, relevant_exception_types)

        if not existing_dependent_errors:
            self._handle_values(model_instance, values, stage, exceptions)

    @abstractmethod
    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        pass
