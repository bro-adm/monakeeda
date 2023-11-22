from abc import ABC, abstractmethod
from typing import ClassVar, List, Type

from monakeeda.consts import NamespacesConsts
from monakeeda.utils import get_items_from_list


class ValuesHandler(ABC):
    __pass_on_errors__: ClassVar[List[Type[Exception]]] = []

    def handle_values(self, model_instance, values, stage):
        exceptions = [type(e) for e in getattr(model_instance, NamespacesConsts.EXCEPTIONS)]
        existing_dependent_errors = get_items_from_list(self.__pass_on_errors__, exceptions)

        if not existing_dependent_errors:
            self._handle_values(model_instance, values, stage)

    @abstractmethod
    def _handle_values(self, model_instance, values, stage):
        pass
