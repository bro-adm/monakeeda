from abc import ABC

from monakeeda.base import GenericAnnotation
from .consts import KnownLabels
from ..existence_managers import CreateFrom


class BaseTypeManagerAnnotation(GenericAnnotation, ABC):
    __manage_all_sub_annotations__ = True
    __prior_handler__ = CreateFrom.label

    @classmethod
    @property
    def label(cls) -> str:
        return KnownLabels.TYPE_MANAGER

    def is_collision(self, other) -> bool:
        super().is_collision(other)
        return False
