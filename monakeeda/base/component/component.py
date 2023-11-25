import inspect
from abc import ABC, abstractmethod
from typing import ClassVar, TypeVar, Type, Any, List

from ..exceptions_manager import ExceptionsDict
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

    @classmethod
    @property
    @abstractmethod
    def label(cls) -> str:
        pass

    @property
    @abstractmethod
    def representor(self) -> str:
        pass

    @property
    @abstractmethod
    def scope(self) -> str:
        pass

    def _extract_relevant_exceptions(self, exceptions: ExceptionsDict) -> List[Exception]:
        return exceptions[self.scope]  # default implementation

    def is_collision(self, other) -> bool:
        if self.label != other.label:
            raise NotImplemented

        return True  # default implementation

    @abstractmethod
    def accept_operator(self, operator_visitor: OperatorVisitor, context: Any):
        pass

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        monkey_cls.scopes[self.scope][self.label].append(self)


TComponent = TypeVar('TComponent', bound=Type[Component])
