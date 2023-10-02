import inspect
from typing import List

from monakeeda.consts import FieldConsts, NamespacesConsts, PythonNamingConsts
from monakeeda.utils import deep_update, get_ordered_set_list
from .base_fields import Field, NoField
from ..component import ComponentManager


class FieldManager(ComponentManager):

    def _components(self, monkey_cls) -> List[Field]:
        field_components = \
            list(
                filter(
                    lambda x: True if x else False,
                    [field_info.get(FieldConsts.FIELD, None) for field_info in
                     monkey_cls.__map__[NamespacesConsts.FIELDS].values()]
                )
            )

        components = []
        for field in field_components:
            components.extend(field._components(monkey_cls))

        components.extend(field_components)

        return components

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

            value._field_key = field_key
            for param in value._components(monkey_cls):
                param._field_key = field_key

            monkey_attrs[field_key] = value
            monkey_cls.__map__[NamespacesConsts.FIELDS][field_key][FieldConsts.FIELD] = value

    def _set_by_base(self, monkey_cls, base, attrs):
        monkey_cls.__map__[NamespacesConsts.FIELDS_KEYS].extend(base.__map__[NamespacesConsts.FIELDS_KEYS])
        base_fields_info = base.__map__[NamespacesConsts.FIELDS]
        deep_update(monkey_cls.__map__[NamespacesConsts.FIELDS], base_fields_info)

    def build(self, monkey_cls, bases, monkey_attrs):
        monkey_cls.__map__.setdefault(NamespacesConsts.FIELDS_KEYS, [])
        super(FieldManager, self).build(monkey_cls, bases, monkey_attrs)
