from typing import Type

from .component import Component


def managed_by(*managers: Type[Component]):
    def get_component(component_cls: Type[Component]):
        for manager in managers:
            manager.__managed_components__.append(component_cls)

        return component_cls

    return get_component
