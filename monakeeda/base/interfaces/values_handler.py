from abc import ABC, abstractmethod
from typing import List

from ..exceptions_manager import ExceptionsDict


class ValuesHandler(ABC):
    @abstractmethod
    def _extract_relevant_exceptions(self, exceptions: ExceptionsDict) -> List[Exception]:
        pass

    def handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        relevant_exceptions = self._extract_relevant_exceptions(exceptions)

        if not relevant_exceptions:
            self._handle_values(model_instance, values, stage, exceptions)

    @abstractmethod
    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        pass
