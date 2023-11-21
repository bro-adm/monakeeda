from abc import ABC
from typing import Dict, List, Union, ClassVar, Type, Generic, Any, Tuple

from .component import Component
from .parameter_component import TParameter
from ..interfaces import MonkeyBuilder


class OneComponentPerLabelAllowedException(Exception):
    def __init__(self, duplicate_labels_components: Dict[str, List[Component]]):
        self.duplicate_labels_components: Dict[str, List[Component]] = duplicate_labels_components

    def __str__(self):
        duplication_description = f"Following components can not be set together -> "

        for label, components in self.duplicate_labels_components.items():
            components_descriptions = [str(component) for component in components]
            duplication_description = duplication_description + f"\n {components_descriptions} -> label: {label}"

        return duplication_description


class OneComponentPerLabelValidatorBuilder(MonkeyBuilder):

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: List[Exception], main_builder: "ConfigurableComponent"):
        existing_labels: Dict[str, Component] = {}
        duplicate_labels_components: Dict[str, List[Component]] = {}

        for nested_component in main_builder._parameters:
            label = nested_component.__label__
            if label in existing_labels:
                duplicate_labels_components.setdefault(label, [existing_labels[label]])
                duplicate_labels_components[label].append(nested_component)
            else:
                existing_labels[label] = nested_component

        if duplicate_labels_components:
            exceptions.append(OneComponentPerLabelAllowedException(duplicate_labels_components))


class UnmatchedParameterKeyException(Exception):
    def __init__(self, unmatched_params: dict):
        self.unmatched_params = unmatched_params

    def __str__(self):
        return f"The following parameters do not have an implementation in the field they are trying to be initialized in  -> {self.unmatched_params}"


class NoUnmatchedParameterKeyValidatorBuilder(MonkeyBuilder):

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: List[Exception], main_builder: "ConfigurableComponent"):
        if main_builder._unused_params:
            exceptions.append(UnmatchedParameterKeyException(main_builder._unused_params))


class ConfigurableComponent(Component, Generic[TParameter], ABC):
    """
    A component that is built from sub components -> the Parameter Components.
    The Configurable Component allows for a set of parameter components which each has a unique key.

    Support for dynamic addition of Parameters is done via the parameter classmethod decorator.

    Usually if not always will Parameter Components be client configurable and accessible objects.
    Initialization of such a class includes validations no responsibility collisions and no unsupported parameter.
    Initialization can look different for each type of a Configurable Component so the main "hidden" API is the override_init method.
    The Component Managers are the ones to actually use this hidden API and actually start the class.
    """

    __builders__: List[MonkeyBuilder] = [OneComponentPerLabelValidatorBuilder(), NoUnmatchedParameterKeyValidatorBuilder()]
    __parameter_components__: List[Type[TParameter]] = []

    @classmethod
    def parameter(cls, parameter: Type[TParameter]):
        """
        A decorator to add parameters into the current cls __parameters_components__ attr

            - overrides according to key.
            - allows priority inserting levels.
        """

        added = False
        cls.__parameter_components__ = list(cls.__parameter_components__)

        for i in range(len(cls.__parameter_components__)):
            exisisting_param = cls.__parameter_components__[i]
            if parameter.__key__ == exisisting_param.__key__:
                cls.__parameter_components__[i] = parameter
                added = True

        if not added:
            cls.__parameter_components__.append(parameter)

        return parameter

    def __init_subclass__(cls, copy_parameter_components=True):
        """
        copy_parameter_components -> False ->
            - will keep the same list memory context as the current Component cls itself.
            - if in the inheriting cls you override some parameter component so the same will happen to all base
              classes with the same memory dict.
        """
        super().__init_subclass__()

        if copy_parameter_components:
            cls.__parameter_components__ = cls.__parameter_components__.copy()

    @classmethod
    def override_init(cls, parameters: List[TParameter], unused_params: Dict[str, Any]):
        instance = cls()
        instance._parameters = parameters
        instance._unused_params = unused_params

        return instance

    def __init__(self, **params):
        # Pretty init for client's sake
        # Generally the override_init is the correct init api and holds the actual necessary attrs
        self._init_params = params

    @classmethod
    def initiate_params(cls, params: dict, **kwargs) -> Tuple[List[TParameter], Dict[str, Any]]:
        initialized_params = []
        unused_params = {}

        for param_key, param_val in params.items():
            for possible_param in cls.__parameter_components__:
                if param_key == possible_param.__key__:
                    initialized_param = possible_param(param_val, **kwargs)
                    initialized_params.append(initialized_param)
                    break

                if possible_param == cls.__parameter_components__[-1]:  # end
                    unused_params[param_key] = param_val

        # if __parameters_components__ is empty so unused_params will be empty
        return initialized_params, unused_params
