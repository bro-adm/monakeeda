from abc import ABC, abstractmethod
from typing import ClassVar, TypeVar, Type

from monakeeda.consts import NamespacesConsts
from .rules import Rules


# TODO: add success type of type bool for type hints

class Component(ABC):
    __label__: ClassVar[str]
    __rules__: ClassVar[Rules] = Rules([])

    def _validate(self, monkey_cls, bases, monkey_attrs) -> bool:
        # TODO: try to use self.__class__.__rules__ for logic consistency
        """
        Pipeline ? -> step X (?)

        :return: True if valid and False if Errors occurred
        """

        exceptions = self.__rules__.validate(self)
        monkey_attrs[NamespacesConsts.BUILD][NamespacesConsts.EXCEPTIONS] = exceptions

        if exceptions:
            return False

        return True

    def _set_cls_landscape(self, monkey_cls, bases, monkey_attrs):
        """
        Pipeline ModelCls Build -> step X (?)

        :param monkey_cls: the MonkeyModel class itself
        :param bases: all the classes the MonkeyModel inherited from
        :param monkey_attrs: all the attributed the MonkeyModel holds

        :return: updated MonkeyModel attributes
        """

        self._monkey_cls = monkey_cls

    def build(self, monkey_cls, bases, monkey_attrs) -> bool:
        is_valid = self._validate(monkey_cls, bases, monkey_attrs)

        if not is_valid:
            return is_valid

        self._set_cls_landscape(monkey_cls, bases, monkey_attrs)

        return True

    @abstractmethod
    def values_handler(self, key, model_instance, values) -> dict:
        # TODO: add key param description
        # TODO: type validations happen at this stage so how come they cant return RulesException
        # TODO: validate if the method should be based on returns or inner method updates

        """
        Pipeline step X (?)

        Some Component implementations do not need and cannot and do not see the full values dictionary given to Model
        on init, so merging the values to the main values dictionary is up to the Manager Component implementation.

        :param key: ?
        :param model_instance: MonkeyModel -> do all components receive the instance?
        :param values: values to initiate component

        :return: updated values
        """

        pass

    def __str__(self):
        return f"{self.__label__} component"


TComponent = TypeVar('TComponent', bound=Type[Component])
