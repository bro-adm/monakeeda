from abc import ABC

from monakeeda.base import GenericAnnotation
from .consts import KnownLabels


class BaseTypeManagerAnnotation(GenericAnnotation, ABC):
    __manage_all_sub_annotations__ = True

    @classmethod
    @property
    def label(cls) -> str:
        return KnownLabels.TYPE_MANAGER
