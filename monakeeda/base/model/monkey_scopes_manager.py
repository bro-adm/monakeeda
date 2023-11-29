from collections import defaultdict
from itertools import combinations
from typing import List, Dict, Set

from .errors import ScopedLabeledComponentsCollisionsException
from ..component import Component
from ..exceptions_manager import ExceptionsDict
from ..meta import ScopesManager
from ..scope import ScopesDict


class MonkeyScopesManager(ScopesManager):
    """

    a: Union[Negative[int], Positive[int]] = Field(lt=-10, gt=50) -> should fail because very combo in both paths fails

    a: Union[Negative[int], Positive[int]] = Field(lt=10, gt=-50) ->
        a.Union0 ->
            negative, int, lt, gt -> combos (numeric_constraint) -> [(negative, lt), (negative, gt), (lt, gt)]
            labels_success_info = {numeric_constraint: (is_success=True, [(negative, lt)])}
        a.Union1 ->
            positive, int(diff), lt, gt -> combos (numeric_constraint) -> [(positive, lt), (positive, gt), (lt, gt)]
            labels_success_info = {numeric_constraint: (is_success=True, [(positive, gt)])}

    b: Union[EmailStr, int] = Field(regex="lol", gt=50) ->
        b.Union0 ->
            EmailStr, regex -> fail
        b.Union1 ->
            int, gt -> success

    """

    def _manage_label_duplications(self, main_scope: str, scoped_components: ScopesDict, exceptions: ExceptionsDict):
        problematic_labeled_collisions: Dict[str, Set[str]] = defaultdict(lambda: set(), {})
        # labels_success_info: Dict[str, Tuple[bool, List[Tuple[Component, Component]]]] = {}

        for scope, scope_info in scoped_components.items():
            for label, components in scope_info.items():
                # is_success = False
                # combo_component_collisions = []

                components: List[Component]

                components_combos = list(combinations(components, 2))
                for combo in components_combos:
                    component_one, component_two = combo
                    if component_one.is_collision(component_two):
                        # combo_component_collisions.append(combo)
                        problematic_labeled_collisions[label].add(component_one.representor)
                        problematic_labeled_collisions[label].add(component_two.representor)
                    # else:
                    #     is_success = True

                # labels_success_info[label] = (is_success, combo_component_collisions)

            # for label, success_info in labels_success_info.items():
            #     is_success, combo_component_collisions = success_info
            #
            #     if not is_success:
            #         for combo in combo_component_collisions:
            #             component_one, component_two = combo
            #             problematic_labeled_collisions[label].add(component_one.representor)
            #             problematic_labeled_collisions[label].add(component_two.representor)
            #     else:

        for label, collisions in problematic_labeled_collisions.items():
            exceptions[main_scope].append(ScopedLabeledComponentsCollisionsException(label, collisions))
