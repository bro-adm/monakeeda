from abc import ABC
from collections import defaultdict
from typing import Dict, List, Tuple, Type

from monakeeda.base import MonkeyBuilder, ConfigParameter, Component, ExceptionsDict, get_parameter_type_by_key, \
    ConfigurableComponent, Parameter
from monakeeda.consts import NamespacesConsts, FieldConsts


class ComponentsDontAcknowledgeParameterKeyException(Exception):
    def __init__(self, component: Component, parameter_key: str, unacknowledged_mapping: Dict[str, str]):
        self.component_representor = component.representor
        self.parameter_key = parameter_key
        self.unacknowledged_mapping = unacknowledged_mapping

    def __str__(self):
        return f"{self.component_representor} dependent on fields to acknowledge key {self.parameter_key} but not all do :( -> {self.unacknowledged_mapping}"


class BaseParameterTypesExtractor(MonkeyBuilder, ABC):
    def __init__(self, *parameter_keys: str, missing_is_exception=True):
        self.parameter_keys = parameter_keys
        self.missing_is_exception = missing_is_exception

    def _map_components_acknowledgment(self, parameter_key: str, components: List[ConfigurableComponent]) -> Tuple[Dict[str, Type[Parameter]], Dict[str, str]]:
        parameters_mapping = {}  # scope: parameter_type
        unacknowledged_mapping = {}  # scope: field.representor

        for component in components:
            parameter_type = get_parameter_type_by_key(component.__class__, parameter_key)
            if parameter_type:
                parameters_mapping[component.scope] = parameter_type
            else:
                unacknowledged_mapping[component.scope] = component.representor

        return parameters_mapping, unacknowledged_mapping


class FieldsParameterTypesExtractor(BaseParameterTypesExtractor):
    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder: ConfigParameter):
        fields = [field_info[FieldConsts.FIELD] for field_info in monkey_cls.struct[NamespacesConsts.FIELDS]]

        all_parameters_mapping = {}

        for parameter_key in self.parameter_keys:
            parameters_mapping, unacknowledged_mapping = self._map_components_acknowledgment(parameter_key, fields)

            if self.missing_is_exception and unacknowledged_mapping:
                exception = ComponentsDontAcknowledgeParameterKeyException(main_builder, parameter_key, unacknowledged_mapping)
                exceptions[main_builder.scope].append(exception)

            all_parameters_mapping[parameter_key] = parameters_mapping

        main_builder._all_parameters_mapping = all_parameters_mapping