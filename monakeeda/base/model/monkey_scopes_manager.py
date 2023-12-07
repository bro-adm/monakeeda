from collections import defaultdict
from itertools import combinations
from typing import List, Dict, Set

from .errors import ScopedLabeledComponentsCollisionsException
from ..component import Component
from ..exceptions_manager import ExceptionsDict
from ..meta import ScopesManager
from ..scope import ScopeDict
from ...utils import get_items_from_list


class MonkeyScopesManager(ScopesManager):
    def _manage_label_duplications(self, main_scope: str, labeled_components: ScopeDict, exceptions: ExceptionsDict):
        problematic_labeled_collisions: Dict[str, Set[str]] = defaultdict(lambda: set(), {})

        for label, components in labeled_components.items():
            components: List[Component]

            components_combos = list(combinations(components, 2))

            for combo in components_combos:
                component_one, component_two = combo

                if ((not component_one.managers and not component_two.managers) or get_items_from_list(component_one.managers, component_two.managers)) and component_one.is_collision(component_two):
                    problematic_labeled_collisions[label].add(component_one.representor)
                    problematic_labeled_collisions[label].add(component_two.representor)

        for label, collisions in problematic_labeled_collisions.items():
            exceptions[main_scope].append(ScopedLabeledComponentsCollisionsException(label, collisions))
