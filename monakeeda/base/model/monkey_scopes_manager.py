from collections import defaultdict
from itertools import combinations
from typing import List, Dict, Set

from .errors import ScopedLabeledComponentsCollisionsException
from ..component import Component
from ..exceptions_manager import ExceptionsDict
from ..meta import ScopesManager
from ..scope import ScopeDict


class MonkeyScopesManager(ScopesManager):
    def _manage_label_duplications(self, scope: str, scope_info: ScopeDict, exceptions: ExceptionsDict):
        problematic_labeled_collisions: Dict[str, Set[str]] = defaultdict(lambda: set(), {})

        for label, components in scope_info.items():
            components: List[Component]

            components_combos = list(combinations(components, 2))
            for combo in components_combos:
                component_one, component_two = combo
                if component_one.is_collision(component_two):
                    problematic_labeled_collisions[label].add(component_one.representor)
                    problematic_labeled_collisions[label].add(component_two.representor)

        for label, collisions in problematic_labeled_collisions.items():
            exceptions[scope].append(ScopedLabeledComponentsCollisionsException(label, collisions))
