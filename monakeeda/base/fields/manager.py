import inspect
from collections import OrderedDict
from typing import List

from monakeeda.consts import FieldConsts, NamespacesConsts, PythonNamingConsts
from monakeeda.utils import deep_update
from .base_fields import Field, NoField, FieldParameter
from ..component import ConfigurableComponentManager


class FieldManager(ConfigurableComponentManager[FieldParameter]):

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
            components.extend(field._parameters)

        components.extend(field_components)

        return components

    def _set_by_base(self, monkey_cls, base, attrs, collisions):
        current_annotations_keys = set(attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS].keys())  # prior bases merged set of fields
        base_annotations_keys = set(base.struct[NamespacesConsts.FIELDS].keys())  # current base set of fields

        collided_fields = current_annotations_keys & base_annotations_keys  # intersection
        for field_key in collided_fields:
            current_field = monkey_cls.struct[NamespacesConsts.FIELDS][field_key].setdefault(FieldConsts.FIELD, None)
            current_parameters = current_field._parameters if current_field else []
            current_field_type = type(current_field) if current_field else None

            base_field = base.struct[NamespacesConsts.FIELDS][field_key].setdefault(FieldConsts.FIELD, None)
            base_parameters = base_field._parameters if base_field else []
            base_field_type = type(base_field) if base_field else None

            if current_field_type and base_field_type and current_field_type!=base_field_type:
                if current_field_type == NoField:
                    monkey_cls.struct[NamespacesConsts.FIELDS][field_key][FieldConsts.FIELD] = base_field
                else:
                    no_field = NoField()
                    no_field._field_key = field_key
                    monkey_cls.struct[NamespacesConsts.FIELDS][field_key][FieldConsts.FIELD] = no_field

            else:
                merged_parameters = self._manage_parameters_inheritance(base_parameters, current_parameters, collisions, is_bases=True)
                merged_field = base_field_type(merged_parameters, unused_params={})
                merged_field._field_key = field_key
                for param in merged_field._parameters:
                    param._field_key = field_key
                monkey_cls.struct[NamespacesConsts.FIELDS][field_key][FieldConsts.FIELD] = merged_field

        new_fields_keys = base_annotations_keys - current_annotations_keys
        for new_field_key in new_fields_keys:
            new_field = base.struct[NamespacesConsts.FIELDS][new_field_key][FieldConsts.FIELD]
            monkey_cls.struct[NamespacesConsts.FIELDS].setdefault(new_field_key, {FieldConsts.FIELD: new_field, FieldConsts.COMPONENTS: []})

    def _set_curr_cls(self, monkey_cls, bases, monkey_attrs):
        annotations: dict = monkey_attrs.get(PythonNamingConsts.annotations, {})  # new or updated fields

        for field_key in annotations:
            monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS].setdefault(field_key, {})
            bases_field = monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][field_key].setdefault(FieldConsts.FIELD, None)
            bases_parameters = bases_field._parameters if bases_field else []
            bases_field_type = type(bases_field) if bases_field else None

            value = monkey_attrs.get(field_key, inspect._empty)

            if not isinstance(value, Field):
                if value is inspect._empty:
                    value = NoField()
                else:
                    value = Field.init_from_params(default=value)

            if bases_field_type and type(value)!=NoField and type(value)==bases_field_type:
                merged_parameters = self._manage_parameters_inheritance(bases_parameters, value._parameters)
                merged_field = Field(merged_parameters, value._unused_params)
            else:
                merged_field = value

            merged_field._field_key = field_key
            for param in merged_field._parameters:
                param._field_key = field_key

            monkey_attrs[field_key] = merged_field
            monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][field_key][FieldConsts.FIELD] = merged_field
            monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][field_key][FieldConsts.COMPONENTS] = []

    def build(self, monkey_cls, bases, monkey_attrs):
        monkey_attrs[NamespacesConsts.STRUCT].setdefault(NamespacesConsts.FIELDS, OrderedDict())
        super(FieldManager, self).build(monkey_cls, bases, monkey_attrs)
