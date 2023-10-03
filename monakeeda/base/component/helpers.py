from collections import OrderedDict
from typing import List, Type, Dict

from .component import Component, all_components
from .configurable_component import ConfigurableComponent
from .parameter_component import Parameter


def organize_components(monkey_components: List[Component]) -> Dict[Type[Component], List[Component]]:
    ordered_dict = OrderedDict()

    for component_type in all_components:
        tmp = []

        for component in monkey_components:
            if str(type(component)) == component_type:
                tmp.append(component)

        ordered_dict[component_type] = tmp

    return ordered_dict


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
