from typing import List

from .component import Component, all_components


def organize_components(monkey_components: List[Component]) -> List[Component]:
    ordered_list = []

    for component_type in all_components:
        for component in monkey_components:
            if str(type(component)) == component_type:
                ordered_list.append(component)

    return ordered_list
