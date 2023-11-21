import inspect
from abc import ABC, abstractmethod
from typing import ClassVar, TypeVar, Type, List, Any

from monakeeda.consts import NamespacesConsts
from monakeeda.utils import get_items_from_list
from ..interfaces import ValuesHandler, MonkeyBuilder
from ..operator import OperatorVisitor

all_components = []


class Component(MonkeyBuilder, ValuesHandler, ABC):
    """
    This is the core logic of Monakeeda, this is what actually runs on every operation you want (from init to openapi spec)

    That being said there are known core methodologies which are:
        - the validations of itself according to client configurable stuff and other components -> RulesValidator.
        - the building of the monkey model -> from just adding itself to a used list,
          up to generating more components and putting them in the correct place -> MonkeyBuilder.
        - handling values in init and update stages-> ValuesHandler.

    Other operations, some which are pre implemented and some which can be a custom implementation are still allowed.
    They are provided via the Visitor design pattern, to allow as much extendability without touching or overriding any component.
    The operator accesses via accept_operator method.
    """

    __prior_handler__: ClassVar[Type['Component']] = None
    __pass_on_errors__: ClassVar[List[Type[Exception]]] = []  # for know provides simplistic logic for passing on handle_values logic according to prior exceptions of dependent components

    def __init_subclass__(cls):
        """
        One of Monakeeda's core concept is to have a components run order.
        That means supporting the chain of responsibility design in a dynamic library that can be extended outside of this project.
        To do that any inheriting class is listed in the all_components list and indexed via the __prior_handler__ attr.
        Do note that inside any lone project, this would effect the import order directly.
        On outer project extensions this is supported via finding the already indexed prior component and inserting this component after it.
        """

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
