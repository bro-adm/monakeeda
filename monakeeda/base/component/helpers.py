from typing import Optional, List

from .component import Component
from .component_decorators import ComponentDecorator


def get_run_decorator(component: Component) -> List[ComponentDecorator]:
    decorators = []

    if component.actuator:
        info = component.managers[component.actuator]

        if isinstance(info, ComponentDecorator):
            decorators.append(info)

        decorators.extend(get_run_decorator(component.actuator))

    return decorators
