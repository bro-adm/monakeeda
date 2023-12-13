import inspect
from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import ClassVar, TypeVar, Type, Any, List, Dict, Optional, OrderedDict as TypeOrderedDict, Set

from .errors import PrioriHandlerCollisionException
from ..exceptions_manager import ExceptionsDict
from ..interfaces import ValuesHandler, MonkeyBuilder
from ..operator import OperatorVisitor

labeled_components: TypeOrderedDict[str, list] = OrderedDict({})


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
    __managed_components__: ClassVar[List[Type['Component']]] = []

    def __init_subclass__(cls, copy_managed_component=True):
        """
        One of Monakeeda's core concept is to have a components run order.
        That means supporting the chain of responsibility design in a dynamic library that can be extended outside of this project.
        To do that any inheriting class is listed in the all_components list and indexed via the __prior_handler__ attr.
        Do note that inside any lone project, this would effect the import order directly.
        On outer project extensions this is supported via finding the already indexed prior component and inserting this component after it.

        Regarding copy_managed_components -> if True it copies the current list to not share reference with subclasses
        """

        super().__init_subclass__()

        if copy_managed_component:
            cls.__managed_components__ = cls.__managed_components__.copy()

        if not inspect.isabstract(cls):
            global labeled_components

            listed_components = list(labeled_components.keys())
            if cls.__prior_handler__ not in labeled_components:
                if cls.label not in labeled_components:
                    labeled_components[cls.label] = [cls]
                else:
                    labeled_components[cls.label].append(cls)
            else:
                if cls.label in labeled_components:
                    set_position = listed_components.index(cls.label)
                    if listed_components[set_position-1] != cls.__prior_handler__:
                        raise PrioriHandlerCollisionException(cls, cls.label, cls.__prior_handler__)

                    labeled_components[cls.label].append(cls)
                else:
                    labeled_components[cls.label] = [cls]

    @classmethod
    @property
    @abstractmethod
    def label(cls) -> str:
        pass

    def __init__(self):
        self.decorator = None  # the decorator that this component might set on its managed components
        self.actuators: Set['Component'] = set()
        self.managers: Dict['Component', Optional['ComponentDecorator']] = {}
        self.managing: List['Component'] = []

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
            raise NotImplementedError

        return True  # default implementation

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        # default implementation
        from .managed_component import handle_manager_collisions

        for managed_component_type in self.__managed_components__:
            components = [component for component in monkey_cls.__label_organized_components__[managed_component_type.label] if type(component) == managed_component_type]

            for component in components:
                if component.scope == self.scope:
                    handle_manager_collisions(self, component, decorator=self.decorator)

    def build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder=None):
        super().build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)
        monkey_cls.scopes[self.scope][self.label].append(self)  # Add regardless of build exceptions - for label collision validation

    @abstractmethod
    def accept_operator(self, operator_visitor: OperatorVisitor, context: Any):
        pass


TComponent = TypeVar('TComponent', bound=Type[Component])
