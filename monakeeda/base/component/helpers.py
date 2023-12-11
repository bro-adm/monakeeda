from typing import List, Set

from .component import Component
from .component_decorators import ComponentDecorator


def get_decorators_per_actuator(main_component: Component) -> List[List[ComponentDecorator]]:
    def _get_decorators_per_actuator(current_route: list, curr_component: Component = None):
        if curr_component and curr_component.decorator:
            current_route.append(curr_component.decorator)

        curr_component = curr_component if curr_component else main_component
        if not curr_component.actuators:
            pass
        elif len(curr_component.actuators) == 1:
            _get_decorators_per_actuator(current_route, curr_component.actuators[0])
        else:
            for actuator in curr_component.actuators:
                actuator_decorations = []
                _get_decorators_per_actuator(actuator_decorations, actuator)

                current_route.append(actuator_decorations)

    def _clean_decorators_routes(routes: list) -> List[List[ComponentDecorator]]:
        final = []
        for item in routes:
            if isinstance(item, list):
                final.extend(_clean_decorators_routes(item))
            else:
                final.append(routes)
                break

        return final

    routes = []
    _get_decorators_per_actuator(routes)
    return _clean_decorators_routes(routes)


def get_all_decorators(component: Component) -> Set[ComponentDecorator]:
    decorators = set()

    for manager, decorator in component.managers.items():
        if decorator:
            decorators.add(decorator)

        if manager.managers:
            decorators.update(get_all_decorators(manager))

    return decorators
