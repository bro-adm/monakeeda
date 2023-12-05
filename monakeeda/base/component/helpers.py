from typing import Optional

from .component import Component
from .component_decorators import ComponentDecorator


def get_run_decorator(component: Component) -> Optional[ComponentDecorator]:
    if component.actuator:
        info = component.managers[component.actuator]
        if not info:
            return None

        if isinstance(info, ComponentDecorator):
            return info

        return get_run_decorator(component.actuator)

    return None
