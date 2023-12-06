from collections import OrderedDict, defaultdict
from itertools import islice
from typing import List, Dict, Type, Optional, Tuple

from monakeeda.consts import NamespacesConsts, FieldConsts
from ..component import Component
from ..meta import ComponentsOrganizer
from ..scope import extract_all_components_of_main_scope


class MonkeyComponentsOrganizer(ComponentsOrganizer):
    """
    The Main organizer logic.

    Manages global and field scoped ordering and includes dependencies as a factor in the organization process.

    The per method docs are great :)
    """

    def __init__(self, ordered_component_types: Dict[str, List[Type[Component]]]):
        self._ordered_component_types = ordered_component_types

    def _get_management_depth(self, component: Component, monkey_components: List[Component]):
        # WE THANK CHAT-GPT for this specific func implementation :) -> Bros mind was melting for some reason

        # Base case: no managed types
        if not component.__managed_components__:
            return 0

        # Recursive case: find the maximum depth among managed types
        max_depth = 0
        for managed_component_type in component.__managed_components__:
            managed_component = next((comp for comp in monkey_components if type(comp) == managed_component_type), None)
            if managed_component:
                depth = 1 + self._get_management_depth(managed_component, monkey_components)
                max_depth = max(max_depth, depth)

        return max_depth

    def _order_by_management_dependencies(self, main_label: str, monkey_components: List[Component]) -> List[Component]:
        def _custom_sorting_key(component):
            return self._get_management_depth(component, monkey_components)

        return sorted(monkey_components, key=_custom_sorting_key, reverse=True)
        # return monkey_components

    def order_by_chain_of_responsibility(self, monkey_components: List[Component]) -> Dict[str, List[Component]]:
        ordered_dict = OrderedDict()

        for label, component_types in self._ordered_component_types.items():
            tmp = []

            for component in monkey_components:
                if type(component) in component_types:
                    tmp.append(component)

            ordered_dict[label] = self._order_by_management_dependencies(label, tmp)

        return ordered_dict

    def _is_attr_level_component(self, monkey_cls, components: List[Component]) -> Optional[bool]:
        if components:
            return components[0].scope in monkey_cls.struct[NamespacesConsts.FIELDS].keys()

        return

    def _find_next_global_scoped_component_type(self, monkey_cls, monkey_type_organized_components: Dict[str, List[Component]]) -> Tuple[Optional[str], int]:
        index = -1

        for label, components in monkey_type_organized_components.items():
            index += 1

            if self._is_attr_level_component(monkey_cls, components) is False:
                return label, index

        return None, -1

    def _order_attr_scoped_components_for_instance_operation_per_field(self, field_key, monkey_cls, attrs_scoped_organized_components: Dict[str, List[Component]]) -> Tuple[List[Component], List[str]]:
        """
        Each field has in the struct namespace all the components that run logic on it.
        These components already appear in the chain of responsibility order due to them being set up in the build logic which works according to it

        Continuing with the sectioning logic explained in the main method, we take only the field's ordered components the current section (the current section is passed via attrs_scoped_organized_components).

        Here we handle dependencies as well -> each field maps it dependencies in the build phase.
        For each dependency we run recursively on it and so on and so on -> USES RECURSION

        we return all the ordered components including the processed dependencies and all the processed field keys.
        """

        organized = []
        processed_fields = []

        dependencies = monkey_cls.struct[NamespacesConsts.FIELDS][field_key][FieldConsts.DEPENDENCIES]
        if dependencies:
            for dependency_key in dependencies:
                organized_dependencies, processed_dependencies = self._order_attr_scoped_components_for_instance_operation_per_field(dependency_key, monkey_cls, attrs_scoped_organized_components)
                organized.extend(organized_dependencies)
                processed_fields.extend(processed_dependencies)

        relevant_scopes, attr_components = extract_all_components_of_main_scope(monkey_cls.scopes, field_key)
        attr_components = [component for component in attr_components if component.label in attrs_scoped_organized_components.keys()]

        organized.extend(attr_components)
        processed_fields.extend(dependencies)
        processed_fields.append(field_key)

        return organized, processed_fields

    def _order_attr_scoped_components_for_instance_operation(self, monkey_cls, attrs_scoped_organized_components: Dict[str, List[Component]]) -> List[Component]:
        """
        Goes over the attrs scoped components received - which are themselves ordered by the type based chained of responsibility.
        For each component type it goes over the components, choosing a field key to start on loosely (dependencies are managed either way)
        uses _order_attr_scoped_components_for_instance_operation_per_field to get the organized components of that field (including dependencies)

        for these sub process we keep a list of processed_attrs -> meaning they were already processed in this current "batch".
        """

        organized = []
        processed_attrs = []

        for label, components in attrs_scoped_organized_components.items():
            for component in components:
                field_key = component.scope

                if field_key not in processed_attrs:
                    _organized, _processed_attrs = self._order_attr_scoped_components_for_instance_operation_per_field(field_key, monkey_cls, attrs_scoped_organized_components)
                    organized.extend(_organized)
                    processed_attrs.extend(_processed_attrs)

        return organized

    def _order_for_instance_operation(self, monkey_cls, monkey_type_organized_components: Dict[str, List[Component]]) -> List[Component]:
        """
        Gets the fully organized dict of components list per component type -> organization based on chain of responsibility setup.
        Generates the components run order list for instance level action such as init and some of the operators.

        USES RECURSION

        sections the organized components into groups that hold a set of attr scoped components and then a global scoped component.
        and so on and so on.

        on each section it runs the _order_attr_scoped_components_for_instance_operation to order those set of components.
        then it adds the global scoped component instances to the final organized list.

        after each section, we compute the next components yet to be processed and run recursively.
        """

        organized_components = []

        next_global_label, next_index = self._find_next_global_scoped_component_type(monkey_cls, monkey_type_organized_components)
        if next_index == -1:
            next_index = len(monkey_type_organized_components)

        attrs_scoped_organized_components = OrderedDict(islice(monkey_type_organized_components.items(), 0, next_index))
        # does not include the global scoped component that exists (or in the last batch does not exist) at the next_index parameter

        sub_organized_components = self._order_attr_scoped_components_for_instance_operation(monkey_cls, attrs_scoped_organized_components)
        organized_components.extend(sub_organized_components)

        if next_global_label:
            organized_components.extend(monkey_type_organized_components[next_global_label])

            next_monkey_type_organized_components = OrderedDict(islice(monkey_type_organized_components.items(), next_index+1, len(monkey_type_organized_components)))
            next_organized_components = self._order_for_instance_operation(monkey_cls, next_monkey_type_organized_components)

            organized_components.extend(next_organized_components)

        return organized_components

    def order_for_instance_operation(self, monkey_cls, monkey_type_organized_components: Dict[str, List[Component]]) -> Dict[Component, bool]:
        """
        calls the above method to get the final run order and then adds the switch on off according to if managed by a component or not
        """

        organized_components = self._order_for_instance_operation(monkey_cls, monkey_type_organized_components)
        managed_components = []

        for component in organized_components:
            managed_components.extend(component.managing)

        return OrderedDict({component: True if component not in managed_components else False for component in organized_components})
