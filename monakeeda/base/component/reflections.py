from typing import Type, List

from .configurable_component import ConfigurableComponent
from .parameter_component import Parameter, ParameterIdentifier


def get_parameter_component_type_by_key(configurable_component: Type[ConfigurableComponent], key: str) -> Type[Parameter]:
    parameter = \
        list(
            filter(
                lambda parameter: parameter.__key__ == key,
                configurable_component.__parameter_components__
            )
        )

    if parameter:
        return parameter[0]

    raise Exception(f'Parameter of key {key} not found in configurable component {configurable_component}')


def get_parameter_component_by_identifier(configurable_component: ConfigurableComponent, identifier: str, identifier_type: ParameterIdentifier) -> Parameter:
    parameter = \
        list(
            filter(
                lambda parameter: getattr(parameter, identifier_type.value) == identifier,
                configurable_component._parameters
            )
        )

    if parameter:
        return parameter[0]

    return
