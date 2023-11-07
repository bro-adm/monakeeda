import inspect
from collections import OrderedDict
from typing import List

from monakeeda.consts import FieldConsts, NamespacesConsts, PythonNamingConsts
from monakeeda.utils import deep_update
from .base_fields import Field, NoField
from ..component import ComponentManager


class FieldManager(ComponentManager):

    def _components(self, monkey_cls) -> List[Field]:
        field_components = \
            list(
                filter(
                    lambda x: True if x else False,
                    [field_info.get(FieldConsts.FIELD, None) for field_info in
                     getattr(monkey_cls, NamespacesConsts.STRUCT)[NamespacesConsts.FIELDS].values()]
                )
            )

        components = []
        for field in field_components:
            components.extend(field._components(monkey_cls))

        components.extend(field_components)

        return components

    def _set_curr_cls(self, monkey_cls, bases, monkey_attrs):
        annotations: dict = monkey_attrs.get(PythonNamingConsts.annotations, {})

        for field_key in annotations:
            monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS].setdefault(field_key, {})
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
            monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][field_key][FieldConsts.FIELD] = value
            monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][field_key][FieldConsts.COMPONENTS] = []

    def _set_by_base(self, monkey_cls, base, attrs):
        base_fields_info = getattr(base, NamespacesConsts.STRUCT)[NamespacesConsts.FIELDS]
        deep_update(attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS], base_fields_info)

    def build(self, monkey_cls, bases, monkey_attrs):
        monkey_attrs[NamespacesConsts.STRUCT].setdefault(NamespacesConsts.FIELDS, OrderedDict())
        super(FieldManager, self).build(monkey_cls, bases, monkey_attrs)
