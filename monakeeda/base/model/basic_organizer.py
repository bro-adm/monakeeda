import inspect
from collections import OrderedDict
from itertools import islice
from typing import List, Dict, Type, Optional, Tuple

from ..meta import ComponentOrganizer
from ..component import Component, all_components
from monakeeda.consts import NamespacesConsts, FieldConsts, ComponentConsts
from monakeeda.utils import insert_if_does_not_exists


class BaseComponentOrganizer(ComponentOrganizer):
    def order_by_chain_of_responsibility(self, monkey_components: List[Component]) -> Dict[Type[Component], List[Component]]:
        ordered_dict = OrderedDict()

        for component_type in all_components:
            tmp = []

            for component in monkey_components:
                if type(component) == component_type:
                    tmp.append(component)

            ordered_dict[component_type] = tmp

        return ordered_dict

    def _is_attr_level_component(self, components: List[Component]) -> Optional[bool]:
        if components:
            return getattr(components[0], ComponentConsts.FIELD_KEY, inspect._empty) != inspect._empty

        return

    def _find_next_global_scoped_component_type(self, monkey_type_organized_components: Dict[Type[Component], List[Component]]) -> Tuple[Type[Component], int]:
        index = -1

        for component_type, components in monkey_type_organized_components.items():
            index += 1

            if self._is_attr_level_component(components) is False:
                return component_type, index

        return None, -1

    def _order_attr_scoped_components_for_instance_operation_per_field(self, field_key, monkey_cls, attrs_scoped_organized_components: Dict[Type[Component], List[Component]]) -> Tuple[List[Component], List[str]]:
        """
        Each field has in the struct namespace all the components that run logic on it.
        These components already apper in the chain of responsibility order due to them being set up in the build logic which works according to it

        Continuing with the sectioning logic explained in the main method, we take only the field's ordered components the current section (the current section is passed via attrs_scoped_organized_components).

        Here we handle dependencies as well -> each field maps it dependencies in the build phase.
        For each dependency we run recursively on it and so on and so on -> USES RECURSION

        we return all the ordered components including the processed dependencies and all the processed field keys.
        """

        organized = []
        processed_fields = []

        dependencies = monkey_cls.struct[NamespacesConsts.FIELDS][field_key].setdefault(FieldConsts.DEPENDENCIES, [])
        if dependencies:
            for dependency_key in dependencies:
                organized_dependencies, processed_dependencies = self._order_attr_scoped_components_for_instance_operation_per_field(dependency_key, monkey_cls, attrs_scoped_organized_components)
                organized.extend(organized_dependencies)
                processed_fields.extend(processed_dependencies)

        attr_components = monkey_cls.struct[NamespacesConsts.FIELDS][field_key][FieldConsts.COMPONENTS]
        attr_components = [component for component in attr_components if type(component) in attrs_scoped_organized_components.keys()]

        organized.extend(attr_components)
        processed_fields.extend(dependencies)
        processed_fields.append(field_key)

        return organized, processed_fields

    def _order_attr_scoped_components_for_instance_operation(self, monkey_cls, attrs_scoped_organized_components: Dict[Type[Component], List[Component]]) -> List[Component]:
        """
        Goes over the attrs scoped components received - which are themselves ordered by the type based chained of responsibility.
        For each component type it goes over the components, choosing a field key to start on loosely (dependencies are managed either way)
        uses _order_attr_scoped_components_for_instance_operation_per_field to get the organized components of that field (including dependencies)

        for these sub process we keep a list of processed_attrs -> meaning they were already processed in this current "batch".
        """

        organized = []
        processed_attrs = []

        for component_type, components in attrs_scoped_organized_components.items():
            for component in components:
                field_key = component._field_key

                if field_key not in processed_attrs:
                    _organized, _processed_attrs = self._order_attr_scoped_components_for_instance_operation_per_field(field_key, monkey_cls, attrs_scoped_organized_components)
                    organized.extend(_organized)
                    processed_attrs.extend(_processed_attrs)

        return organized

    def order_for_instance_operation(self, monkey_cls, monkey_type_organized_components: Dict[Type[Component], List[Component]]) -> List[Component]:
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

        next_global_component_type, next_index = self._find_next_global_scoped_component_type(monkey_type_organized_components)
        if next_index == -1:
            next_index = len(monkey_type_organized_components)

        attrs_scoped_organized_components = OrderedDict(islice(monkey_type_organized_components.items(), 0, next_index))
        # does not include the global scoped component that exists (or in the last batch does not exist) at the next_index parameter

        sub_organized_components = self._order_attr_scoped_components_for_instance_operation(monkey_cls, attrs_scoped_organized_components)
        organized_components.extend(sub_organized_components)

        if next_global_component_type:
            organized_components.extend(monkey_type_organized_components[next_global_component_type])

            next_monkey_type_organized_components = OrderedDict(islice(monkey_type_organized_components.items(), next_index+1, len(monkey_type_organized_components)))
            next_organized_components = self.order_for_instance_operation(monkey_cls, next_monkey_type_organized_components)

            organized_components.extend(next_organized_components)

        return organized_components
