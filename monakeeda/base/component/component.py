from abc import ABC, abstractmethod
from enum import Enum
from typing import ClassVar, TypeVar, Type

from monakeeda.consts import NamespacesConsts
from .rules import Rules


class Stages(Enum):
    INIT = 'init'
    UPDATE = 'update'


class Component(ABC):
    __label__: ClassVar[str]
    __rules__: ClassVar[Rules] = Rules([])
    __priority__: ClassVar[int] = 0

    def _validate(self, monkey_cls, bases, monkey_attrs) -> bool:
        """
        Pipeline ? -> step X (?)

        :return: True if valid and False if Errors occurred
        """

        exceptions = self.__rules__.validate(self, monkey_cls)

        if exceptions:
            monkey_attrs[NamespacesConsts.BUILD][NamespacesConsts.EXCEPTIONS].append_exception(exceptions)

            return False

        return True

    @abstractmethod
    def _set_cls_landscape(self, monkey_cls, bases, monkey_attrs):
        """
        Pipeline ModelCls Build -> step X (?)

        :param monkey_cls: the MonkeyModel class itself
        :param bases: all the classes the MonkeyModel inherited from
        :param monkey_attrs: all the attributed the MonkeyModel holds
        """

        pass

    def build(self, monkey_cls, bases, monkey_attrs) -> bool:
        """
        At the build stage of ALL components you will want validation to take place before setting the landscape :)
        """
        is_valid = self._validate(monkey_cls, bases, monkey_attrs)

        if not is_valid:
            return is_valid

        self._set_cls_landscape(monkey_cls, bases, monkey_attrs)

        return True

    @abstractmethod
    def _values_handler(self, priority, model_instance, values, stage: Stages) -> dict:
        """
        Pipeline step X (?)

        Some Component implementations do not need and cannot and do not see the full values dictionary given to Model
        on init, so merging the values to the main values dictionary is up to the Manager Component implementation.

        :param model_instance: MonkeyModel -> do all components receive the instance?
        :param values: values to initiate component

        :return: updated values
        """

        pass

    def values_handler(self, priority, model_instance, values, stage: Stages) -> dict:
        if self.__priority__ == -1 or self.__priority__ == priority:
            return self._values_handler(priority, model_instance, values, stage)

        return {}

    def __str__(self):
        return f"{self.__label__} component"


TComponent = TypeVar('TComponent', bound=Type[Component])
