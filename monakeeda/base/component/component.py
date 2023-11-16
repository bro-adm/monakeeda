import inspect
from abc import ABC, abstractmethod
from typing import ClassVar, TypeVar, Type, List, Any

from monakeeda.consts import NamespacesConsts
from monakeeda.utils import get_items_from_list
from ..interfaces import ValuesHandler, RulesValidator, MonkeyBuilder
from ..operator import OperatorVisitor

all_components = []


class Component(RulesValidator, MonkeyBuilder, ValuesHandler, ABC):
    __prior_handler__: ClassVar[Type['Component']] = None
    __pass_on_errors__: ClassVar[List[Type[Exception]]] = []

    def __init_subclass__(cls):
        super().__init_subclass__()

        if not inspect.isabstract(cls):
            if cls.__prior_handler__:
                position = all_components.index(cls.__prior_handler__)
                all_components.insert(position + 1, cls)
            else:
                all_components.append(cls)

    def handle_values(self, model_instance, values, stage):
        exceptions = [type(e) for e in getattr(model_instance, NamespacesConsts.EXCEPTIONS)]
        existing_dependent_errors = get_items_from_list(self.__pass_on_errors__, exceptions)

        if not existing_dependent_errors:
            self._handle_values(model_instance, values, stage)

    @abstractmethod
    def _handle_values(self, model_instance, values, stage):
        pass

    @abstractmethod
    def accept_operator(self, operator_visitor: OperatorVisitor, context: Any):
        pass


TComponent = TypeVar('TComponent', bound=Type[Component])
