from abc import ABC, abstractmethod
from typing import Any
from typing_extensions import get_args

from monakeeda.consts import NamespacesConsts, FieldConsts
from .. import Stages
from ..component import Component


class Annotation(Component, ABC):

    def __init__(self, base_type):
        self.base_type = base_type

    # TODO: what happens when value is not provided for a certain key
    def values_handler(self, key, model_instance, values, stage) -> dict:
        field_info = model_instance.__map__[NamespacesConsts.FIELDS][key]

        if stage == Stages.UPDATE:
            # TODO: validate if this effects the class mappings !!!
            field_info[FieldConsts.VALUE] = getattr(model_instance, key)

        return self._act_with_value(values[key], model_instance, field_info, stage)

    def _set_cls_landscape(self, monkey_cls, bases, monkey_attrs):
        monkey_attrs[FieldConsts.TYPE] = self.base_type
        monkey_attrs[FieldConsts.ANNOTATION] = self

    @abstractmethod
    def _act_with_value(self, value, cls, current_field_info, stage) -> Any:
        pass


class GenericAnnotation(Annotation, ABC):
    @property
    def _types(self):
        return get_args(self.base_type)

    def __getitem__(self, item):
        # TODO: add explanation
        return item
