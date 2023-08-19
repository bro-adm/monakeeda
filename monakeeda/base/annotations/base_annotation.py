from abc import ABC, abstractmethod
from typing import Any

from typing_extensions import get_args

from monakeeda.consts import NamespacesConsts, FieldConsts
from ..component import Component, Stages


class Annotation(Component, ABC):
    __label__ = 'annotation'

    def __init__(self, field_key, base_type):
        self._field_key = field_key
        self.base_type = base_type

    # TODO: what happens when value is not provided for a certain key
    def _values_handler(self, model_instance, values, stage) -> dict:
        """
        As I see it, this needs to stand to the components API and so the AnnotationsMainComponent will be the one
        to set the scope of operation of the Annotation implementation instance.

        This basically happens as a result of the instance being per implementation and not per field usage
        as opposed to other components .

        Until that changes it is expected logically to pass the single key,val in the values dict to each run.
        """

        field_info = model_instance.__map__[NamespacesConsts.FIELDS][self._field_key]
        value = values[self._field_key]

        if stage == Stages.UPDATE:
            # TODO: validate if this effects the class mappings !!!
            field_info[FieldConsts.VALUE] = getattr(model_instance, self._field_key)

        return {self._field_key: self._act_with_value(value, model_instance, field_info, stage)}

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
