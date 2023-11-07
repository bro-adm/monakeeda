import inspect
from collections import OrderedDict
from itertools import islice
from typing import List, Dict, Type, Optional, Tuple

from ..meta import ComponentOrganizer
from ..component import Component, all_components
from monakeeda.consts import NamespacesConsts, FieldConsts, ComponentConsts


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

    def _order_attr_scoped_components_for_instance_operation(self, monkey_cls, attrs_scoped_organized_components: Dict[Type[Component], List[Component]]) -> List[Component]:
        """
        goes over the attrs scoped components received.
            goes over each component instance in the different attrs scoped components types it works on currently
                gets the field_key of each and finds all the attrs scoped components in the range that is currently looked on (According to the global scoped components range)

        includes dependencies considerations -> e.g. CreateFrom appears prior to Validation but will look and process the dependencies prior

        for these sub process we keep a list of listed_attrs -> meaning they were already processed in this current "batch".
        """
        # TODO: add dependency considerations

        organized = []
        processed_attrs = []

        for component_type, components in attrs_scoped_organized_components.items():
            for component in components:
                field_key = component._field_key

                if field_key not in processed_attrs:
                    attr_components = monkey_cls.struct[NamespacesConsts.FIELDS][field_key][FieldConsts.COMPONENTS]
                    attr_components = [component for component in attr_components if type(component) in attrs_scoped_organized_components.keys()]
                    # already set in organized order of chain of responsibility due to how the fact that the build stage is run in that order

                    organized.extend(attr_components)

                    processed_attrs.append(field_key)

        # print(processed_attrs)
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

        # print("############")
        # print(monkey_cls.__name__)
        # print(monkey_type_organized_components.keys())
        organized_components = []

        next_global_component_type, next_index = self._find_next_global_scoped_component_type(monkey_type_organized_components)
        if next_index == -1:
            next_index = len(monkey_type_organized_components)

        attrs_scoped_organized_components = OrderedDict(islice(monkey_type_organized_components.items(), 0, next_index))
        # print(attrs_scoped_organized_components.keys(), next_global_component_type)
        # does not include the global scoped component that exists (or in the last batch does not exist) at the next_index parameter

        sub_organized_components = self._order_attr_scoped_components_for_instance_operation(monkey_cls, attrs_scoped_organized_components)
        organized_components.extend(sub_organized_components)

        if next_global_component_type:
            organized_components.extend(monkey_type_organized_components[next_global_component_type])

            next_monkey_type_organized_components = OrderedDict(islice(monkey_type_organized_components.items(), next_index+1, len(monkey_type_organized_components)))
            next_organized_components = self.order_for_instance_operation(monkey_cls, next_monkey_type_organized_components)

            organized_components.extend(next_organized_components)

        return organized_components
