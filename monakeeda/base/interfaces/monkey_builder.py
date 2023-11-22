from abc import ABC, abstractmethod
from typing import List

from ..exceptions_manager import ExceptionsDict


class MonkeyBuilder(ABC):
    __builders__: List["MonkeyBuilder"] = []

    @abstractmethod
    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        pass

    def build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder=None):
        new_exceptions = ExceptionsDict()

        for builder in self.__builders__:
            builder.build(monkey_cls, bases, monkey_attrs, new_exceptions, main_builder=main_builder if main_builder else self)

        if not new_exceptions:
            self._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)

        else:
            for key, key_exceptions in new_exceptions.items():
                exceptions[key].extend(key_exceptions)
