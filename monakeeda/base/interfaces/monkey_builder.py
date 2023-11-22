from abc import ABC, abstractmethod
from typing import List


class MonkeyBuilder(ABC):
    __builders__: List["MonkeyBuilder"] = []

    @abstractmethod
    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: List[Exception], main_builder):
        pass

    def build(self, monkey_cls, bases, monkey_attrs, exceptions: List[Exception], main_builder=None):
        new_exceptions = []

        for builder in self.__builders__:
            if not new_exceptions:
                builder.build(monkey_cls, bases, monkey_attrs, new_exceptions, main_builder=main_builder if main_builder else self)

        if not new_exceptions:
            self._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)

        else:
            exceptions.extend(new_exceptions)
