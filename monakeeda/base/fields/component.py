import inspect
from typing import List

from monakeeda.consts import FieldConsts, NamespacesConsts, PythonNamingConsts
from monakeeda.utils import deep_update, get_ordered_set_list
from .base_fields import Field, NoField, FieldParameter
from ..component import MainComponent


@Field.parameter
class DefaultParameter(FieldParameter):
    __key__: str = 'default'
    __label__ = 'default_provider'

    def values_handler(self, model_instance, values, stage) -> dict:
        return {self._field_key: values.get(self._field_key, self.param_val)}

    def _set_cls_landscape(self, monkey_cls, bases, monkey_attrs):
        super(DefaultParameter, self)._set_cls_landscape(monkey_cls, bases, monkey_attrs)
        monkey_cls.__map__[NamespacesConsts.FIELDS][self._field_key][FieldConsts.REQUIRED] = False


class FieldMainComponent(MainComponent[Field]):

    def _components(self, monkey_cls) -> List[Field]:
        return \
            list(
                filter(
                    lambda x: True if x else False,
                    [field_info.get(FieldConsts.FIELD, None) for field_info in
                     monkey_cls.__map__[NamespacesConsts.FIELDS].values()]
                )
            )

    def _set_curr_cls(self, monkey_cls, bases, monkey_attrs):
        annotations: dict = monkey_attrs.get(PythonNamingConsts.annotations, {})
        monkey_cls.__map__[NamespacesConsts.FIELDS_KEYS] = get_ordered_set_list(annotations.keys())

        for field_key in annotations:
            monkey_cls.__map__[NamespacesConsts.FIELDS].setdefault(field_key, {})
            value = monkey_attrs.get(field_key, inspect._empty)

            if not isinstance(value, Field):
                if value is inspect._empty:
                    value = NoField()
                else:
                    value = Field(default=value)

            # TODO: this sucks
            value._field_key = field_key
            for param in value._components(monkey_cls):
                param._field_key = field_key

            # TODO: make sure I did not fuck up signatures...
            monkey_attrs[field_key] = value
            monkey_cls.__map__[NamespacesConsts.FIELDS][field_key][FieldConsts.FIELD] = value

    def _set_by_base(self, monkey_cls, base, attrs):
        monkey_cls.__map__[NamespacesConsts.FIELDS_KEYS].extend(base.__map__[NamespacesConsts.FIELDS_KEYS])
        base_fields_info = base.__map__[NamespacesConsts.FIELDS]
        deep_update(monkey_cls.__map__[NamespacesConsts.FIELDS], base_fields_info)

    def run_bases(self, monkey_cls, bases, monkey_attrs):
        monkey_cls.__map__.setdefault(NamespacesConsts.FIELDS_KEYS, [])
        super(FieldMainComponent, self).run_bases(monkey_cls, bases, monkey_attrs)
