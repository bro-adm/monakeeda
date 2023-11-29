from abc import ABC

from monakeeda.base import GenericAnnotation, ExceptionsDict
from .consts import KnownLabels


class BaseInfiniteArgsAnnotation(GenericAnnotation, ABC):
    @classmethod
    @property
    def label(cls) -> str:
        return KnownLabels.TYPE_MANAGER

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        super()._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)

        index = 0
        for component in self.represented_annotations:
            component.scope = f"{component.scope}.{self.__class__.__name__}:{index}"
            self.managing.append(component)
            index += 1
