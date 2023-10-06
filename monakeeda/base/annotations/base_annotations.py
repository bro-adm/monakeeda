from abc import ABC

from typing_extensions import get_args

from monakeeda.consts import NamespacesConsts, FieldConsts
from ..component import Component


class Annotation(Component, ABC):

    def __init__(self, field_key, base_type):
        self._field_key = field_key
        self.base_type = base_type

    def build(self, monkey_cls, bases, monkey_attrs):
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.TYPE] = self.base_type
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.ANNOTATION] = self


class GenericAnnotation(Annotation, ABC):
    @property
    def _types(self):
        return get_args(self.base_type)

    def __getitem__(self, item):
        return item
