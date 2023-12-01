from typing import Type, List, Optional

from .component import ConfigurableComponent, Parameter, Component
from .model import BaseMonkey


def get_scoped_components_by_label(monkey: BaseMonkey, scope: str, label: str) -> List[Component]:
    return monkey.scopes[scope][label]


def get_parameter_type_by_key(component: Type[ConfigurableComponent], key: str) -> Optional[Type[Parameter]]:
    for parameter in component.__parameter_components__:
        if parameter.__key__ == key:
            return parameter

    return


def get_all_managed_components(component: Component) -> List[Component]:
    components = []

    components.extend(component.managing)

    for managed_component in component.managing:
        components.extend(get_all_managed_components(managed_component))

    return components
