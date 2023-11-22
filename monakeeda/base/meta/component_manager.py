from abc import ABC, abstractmethod
from typing import List, Generic

from monakeeda.consts import NamespacesConsts
from monakeeda.logger import logger, STAGE, MONKEY
from monakeeda.helpers import ExceptionsDict
from ..component import Component, TParameter
from ..interfaces import MonkeyBuilder


class ComponentManager(MonkeyBuilder, ABC):
    """
    Responsible for inheritance logics for each type of main component and then returning all components under its jurisdiction.
    Inheritance can be tricky at points, so it also manages collisions with it.

    As expected due to its responsibility of finding all components, it also sets up the monkey landscape for them (via build)
    """

    @abstractmethod
    def _components(self, monkey_cls) -> List[Component]:
        pass

    @abstractmethod
    def _set_by_base(self, monkey_cls, base, attrs, collisions: dict):
        pass

    @abstractmethod
    def _set_curr_cls(self, monkey_cls, bases, monkey_attrs):
        pass

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        collisions = {}

        for base in bases:
            logger.info(f"Build By Base {base.__name__}", extra={STAGE: f"{self.__class__.__name__} BUILD", MONKEY: monkey_cls.__name__})
            logger.info(f"\tPrior Collisions = {collisions}", extra={STAGE: f"{self.__class__.__name__} BUILD", MONKEY: monkey_cls.__name__})
            self._set_by_base(monkey_cls, base, monkey_attrs, collisions)

        logger.info(f"Build Current Cls {monkey_cls.__name__}", extra={STAGE: f"{self.__class__.__name__} BUILD", MONKEY: monkey_cls.__name__})
        self._set_curr_cls(monkey_cls, bases, monkey_attrs)

        components = self._components(monkey_cls)
        monkey_attrs[NamespacesConsts.COMPONENTS].extend(components)
        logger.info(f"Final Merged Components = {components}", extra={STAGE: f"{self.__class__.__name__} BUILD", MONKEY: monkey_cls.__name__})


class ConfigurableComponentManager(ComponentManager, ABC, Generic[TParameter]):
    def _manage_parameters_inheritance(self, current_parameters: List[TParameter], new_parameters: List[TParameter], collisions: list = None, is_bases=False) -> List[TParameter]:
        """
        ConfigurableComponents have sub Parameter Components that "build" them.
        When inheriting from another monkey, you dont want to always copy all priorly set parameters.

        This is a helper method to do just that whilst acknowledging the fact that the merge order is from the bases up to the current main cls.

        What can happen with inheritance is either bases collision parameters or main cls overrideable parameters - THERE ARE NO APPEND PARAMETERS.
        What we dont want to happen is to change the configurations of the fields from the inherited classes

        to keep context of previous collision on bases merges you pass the collisions value.
        the value is kept by reference

        each parameter lists will not hold in themselves more than one of the same __key__.

        :returns: Merged Parameters
        """

        merged_parameters = new_parameters.copy()

        # remove previous collisions on bases merges
        if is_bases and collisions:
            for collision_parameter_key in collisions:
                for parameter in merged_parameters:
                    if parameter.__key__ == collision_parameter_key:
                        merged_parameters.remove(parameter)
                        break

        # simple check for collisions/overrides on cls merges or need for "inheritance" into merged_params
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
