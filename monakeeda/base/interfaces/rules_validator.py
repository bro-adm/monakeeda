from abc import ABC
from typing import ClassVar

from .rules import Rules
from monakeeda.consts import NamespacesConsts


class RulesValidator(ABC):
    __rules__: ClassVar[Rules] = Rules([])

    def validate(self, monkey_cls, bases, monkey_attrs):
        exceptions = self.__rules__.validate(self, monkey_cls)

        if exceptions:
            monkey_attrs[NamespacesConsts.EXCEPTIONS].append_exception(exceptions)
