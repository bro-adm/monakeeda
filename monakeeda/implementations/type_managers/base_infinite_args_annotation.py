from abc import ABC

from monakeeda.base import GenericAnnotation, ExceptionsDict
from .consts import KnownLabels


class BaseInfiniteArgsAnnotation(GenericAnnotation, ABC):
    @classmethod
    @property
    def label(cls) -> str:
        return KnownLabels.TYPE_MANAGER
