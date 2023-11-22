from abc import ABC
from typing import Dict, List, Type, Generic, Any, Tuple

from monakeeda.consts import ComponentConsts
from monakeeda.helpers import ExceptionsDict
from .component import Component
from .parameter_component import TParameter
from ..interfaces import MonkeyBuilder


class OneComponentPerLabelAllowedException(Exception):
    def __init__(self, component: "ConfigurableComponent", duplicate_labels_components: Dict[str, List[str]]):
        self.component_representor = component.representor
        self.duplicate_labels_components = duplicate_labels_components

    def __str__(self):
        duplication_description = f"{self.component_representor} does not allow the following components to be set together -> "

        for label, components in self.duplicate_labels_components.items():
            duplication_description = duplication_description + f"\n\t\t Label: {label} -> {components}"

        return duplication_description


class OneComponentPerLabelValidator(MonkeyBuilder):
    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder: "ConfigurableComponent"):
        existing_labels: Dict[str, str] = {}
        duplicate_labels_components: Dict[str, List[str]] = {}

        for nested_component in main_builder._parameters:
            label = nested_component.__label__
            if label in existing_labels:
                duplicate_labels_components.setdefault(label, [existing_labels[label]])
                duplicate_labels_components[label].append(nested_component.__key__)
            else:
                existing_labels[label] = nested_component.__key__

        if duplicate_labels_components:
            exception = OneComponentPerLabelAllowedException(main_builder, duplicate_labels_components)
            exceptions[main_builder.scope].append(exception)


class UnmatchedParameterKeysException(Exception):
    def __init__(self, component: "ConfigurableComponent", unmatched_params: dict):
        self.component_representor = component.representor
        self.unmatched_params = unmatched_params

    def __str__(self):
        return f"{self.component_representor} does not support the following given params -> {self.unmatched_params}"


class NoUnmatchedParameterKeyValidator(MonkeyBuilder):
    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder: "ConfigurableComponent"):
        if main_builder._unused_params:
            exception = UnmatchedParameterKeysException(main_builder, main_builder._unused_params)
            exceptions[main_builder.scope].append(exception)


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

    __builders__: List[MonkeyBuilder] = [OneComponentPerLabelValidator(), NoUnmatchedParameterKeyValidator()]
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
