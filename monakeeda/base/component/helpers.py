from typing import Type

from .configurable_component import ConfigurableComponent
from .parameter_component import Parameter


def get_parameter_component_by_label(configurable_component: Type[ConfigurableComponent], label: str) -> Type[
    Parameter]:
    parameter = \
        list(
            filter(
                lambda parameter: parameter.__label__ == label,
                configurable_component.__parameter_components__
            )
        )

    if parameter:
        return parameter[0]

    raise Exception(f'Parameter of label {label} not found in configurable component {configurable_component}')
