from abc import ABC, abstractmethod
from typing import List, Generic

from monakeeda.consts import NamespacesConsts
from .component import Component
from .parameter_component import TParameter
from .monkey_builder import MonkeyBuilder


class ComponentManager(MonkeyBuilder, ABC):

    @abstractmethod
    def _components(self, monkey_cls) -> List[Component]:
        pass

    @abstractmethod
    def _set_by_base(self, monkey_cls, base, attrs, collisions: dict):
        pass

    @abstractmethod
    def _set_curr_cls(self, monkey_cls, bases, monkey_attrs):
        pass

    def build(self, monkey_cls, bases, monkey_attrs):
        collisions = {}

        for base in bases:
            self._set_by_base(monkey_cls, base, monkey_attrs, collisions)

        self._set_curr_cls(monkey_cls, bases, monkey_attrs)

        components = self._components(monkey_cls)
        monkey_attrs[NamespacesConsts.COMPONENTS].extend(components)


class ConfigurableComponentManager(ComponentManager, Generic[TParameter]):
    def _manage_parameters_inheritance(self, current_parameters: List[TParameter], new_parameters: List[TParameter], collisions: list=None, is_bases=False) -> List[TParameter]:
        """
        Meant for use with the ComponentManagers, in which we have the set by base and set curr cls.
        Each method has the responsibility to manage inheritance itself on the relevant components under its jurisdiction.

        This is a helper method to do just that whilst acknowledging the fact that the merge order is from the bases up to the current main cls.

        What can happen with inheritance is either bases collision parameters or main cls overrideable parameters - THERE ARE NO APPEND PARAMETERS.
        What we dont want to happen is to change the configurations of the fields from the inherited classes

        to keep context of previous collision on bases merges you pass the previous_collisions value.
        the value for it is provided via this method on return

        each parameter lists will not hold in themselves more than one of the same __key__.

        :returns: Merged Parameters, Collision Parameters Keys
        """

        merged_parameters = new_parameters.copy()

        # remove previous collisions on bases merges
        if is_bases and collisions:
            for collision_parameter_key in collisions:
                for parameter in merged_parameters:
                    if parameter.__key__ == collision_parameter_key:
                        merged_parameters.remove(parameter)
                        break

        for current_parameter in current_parameters:
            add_current = True

            for new_parameter in merged_parameters:
                if new_parameter.__key__ == current_parameter.__key__:
                    add_current = False

                    if is_bases:
                        merged_parameters.remove(new_parameter)
                        collisions.append(new_parameter.__key__)

                    break

            if add_current:
                merged_parameters.append(current_parameter)

        return merged_parameters
