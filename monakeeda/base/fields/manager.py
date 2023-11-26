import inspect
from collections import OrderedDict
from typing import List, Type

from monakeeda.consts import FieldConsts, NamespacesConsts, PythonNamingConsts
from monakeeda.helpers import defaultdictvalue
from .base_fields import Field, FieldParameter
from ..exceptions_manager import ExceptionsDict
from ..meta import ConfigurableComponentManager


class FieldManager(ConfigurableComponentManager[FieldParameter]):
    """
    The Fields concept allows for multiple Field classes (one is natively implemented).
    The Field classes types are overrideable via the class name.

    The Fields Manager responsibility, just like most other Component Manager is to find the relevant components, build them
    and manage inheritance collisions.

    attrs might not be configured with a Field directly ot at all.
    At these cases, the Manage is responsible to create one for the attr in order for further compartments to have sane APIs.
    This means having access to a default NoField and Field implementations (can be overriden) with some available sub Parameters.

    By default, all model inheritances will automatically build the current Field classes by:
        - merging the bases parameters with collision management
        - overriding merges via current cls parameters

    There are pre-known namespaces that are set by default by the manager to decrease if-exists logic from other compartments.
    Not all known namespaces are set, because there is no need for such an overload of logic and responsibility.
    """

    def __init__(self, default_field_type: Type[Field], default_no_field_type: Type[Field]):
        self._default_field_type = default_field_type
        self._default_no_field_type = default_no_field_type

    def _components(self, monkey_cls) -> List[Field]:
        fields_info = getattr(monkey_cls, NamespacesConsts.STRUCT)[NamespacesConsts.FIELDS]
        field_components = [field_info[FieldConsts.FIELD] for field_info in fields_info.values()]

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
            field_collisions = collisions.setdefault(field_key, [])

            current_field = monkey_cls.struct[NamespacesConsts.FIELDS][field_key][FieldConsts.FIELD]
            current_parameters = current_field._parameters
            current_field_type = type(current_field)

            base_field = base.struct[NamespacesConsts.FIELDS][field_key][FieldConsts.FIELD]
            base_parameters = base_field._parameters
            base_field_type = type(base_field)

            if field_collisions is True:
                pass  # field already set to no_field

            elif current_field_type != base_field_type:
                if current_field_type == self._default_no_field_type:
                    monkey_cls.struct[NamespacesConsts.FIELDS][field_key][FieldConsts.FIELD] = base_field
                else:
                    no_field = self._default_no_field_type.override_init(field_key, [], {})
                    monkey_cls.struct[NamespacesConsts.FIELDS][field_key][FieldConsts.FIELD] = no_field
                    collisions[field_key] = True

            else:
                merged_parameters = self._manage_parameters_inheritance(base_parameters, current_parameters, field_collisions, is_bases=True)
                merged_field = base_field_type.override_init(field_key, merged_parameters, unused_params={})
                monkey_cls.struct[NamespacesConsts.FIELDS][field_key][FieldConsts.FIELD] = merged_field

        new_fields_keys = base_annotations_keys - current_annotations_keys
        for new_field_key in new_fields_keys:
            new_field = base.struct[NamespacesConsts.FIELDS][new_field_key][FieldConsts.FIELD]
            monkey_cls.struct[NamespacesConsts.FIELDS][new_field_key][FieldConsts.FIELD] = new_field

    def _set_curr_cls(self, monkey_cls, bases, monkey_attrs):
        annotations: dict = monkey_attrs.get(PythonNamingConsts.annotations, {})  # new or updated fields

        for field_key in annotations:
            bases_field = monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][field_key][FieldConsts.FIELD]
            bases_parameters = bases_field._parameters
            bases_field_type = type(bases_field)

            value = monkey_attrs.get(field_key, inspect._empty)

            if not isinstance(value, Field):
                if value is inspect._empty:
                    value = self._default_no_field_type()
                else:
                    value = self._default_field_type.init_from_arbitrary_value(value)

            field_type = type(value)
            initialized_params, unused_params = value.initiate_params(value._init_params, field_key=field_key)

            if field_type == self._default_no_field_type or field_type == bases_field_type:
                merged_parameters = self._manage_parameters_inheritance(bases_parameters, initialized_params)
                merged_field = field_type.override_init(field_key, merged_parameters, unused_params)
            else:
                merged_field = field_type.override_init(field_key, initialized_params, unused_params)

            monkey_attrs[field_key] = merged_field
            monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][field_key][FieldConsts.FIELD] = merged_field

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        default_fields_dict = defaultdictvalue(lambda key: {FieldConsts.DEPENDENCIES: [], FieldConsts.DEPENDENTS: [], FieldConsts.FIELD: self._default_no_field_type.override_init(key, [], {})}, OrderedDict())
        # Do note that this defaultdict does not hurt priorly set bases becasue we never directly ask for a field_info of a base field without knowing it exists there

        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS] = default_fields_dict
        super(FieldManager, self)._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)
