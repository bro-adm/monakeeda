from abc import ABC

from monakeeda.base import FieldParameter


class BaseInputFieldParameter(FieldParameter, ABC):
    __label__ = 'input'
