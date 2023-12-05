from typing import Type

from monakeeda.utils import to_types
from .component import Component


def managed_by(*managers: Type[Component]):
    def get_component(component_cls: Type[Component]):
        for manager in managers:
            manager.__managed_components__.append(component_cls)

        return component_cls

    return get_component


def handle_manager_collisions(main_component: Component, managed_component: Component, decorator=None, collision_by_type=False):
    managers_to_remove = []
    for manager in managed_component.managers:
        if (collision_by_type and type(manager) in to_types(main_component.managers)) or manager in main_component.managers:
            managers_to_remove.append(manager)
    for manager in managers_to_remove:
        manager.managing.remove(managed_component)
        managed_component.managers.pop(manager)

    managed_component.managers[main_component] = decorator if decorator else main_component.managers
    managed_component.is_managed = True
    main_component.managing.append(managed_component)
