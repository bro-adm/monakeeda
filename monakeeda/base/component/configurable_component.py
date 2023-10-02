from abc import ABC
from typing import Dict, List, Union, Generic, ClassVar, Type

from .component import Component, TComponent
from .parameter_component import TParameter, Parameter
from .rules import RuleException, Rule, Rules


class OneComponentPerLabelAllowedRuleException(RuleException):
    def __init__(self, duplicate_labels_components: Dict[str, List[Component]]):
        self.duplicate_labels_components: Dict[str, List[Component]] = duplicate_labels_components

    def __str__(self):
        duplication_description = f"Following components can not be set together -> "

        for label, components in self.duplicate_labels_components.items():
            components_descriptions = [str(component) for component in components]
            duplication_description = duplication_description + f"\n {components_descriptions} -> label: {label}"

        return duplication_description


class OneComponentPerLabelAllowedRule(Rule):

    def validate(self, component: "ConfigurableComponentManager", monkey_cls) -> Union[RuleException, None]:
        existing_labels: Dict[str, Component] = {}
        duplicate_labels_components: Dict[str, List[Component]] = {}

        for nested_component in component._components(monkey_cls):
            label = nested_component.__label__
            if label in existing_labels:
                duplicate_labels_components.setdefault(label, [existing_labels[label]])
                duplicate_labels_components[label].append(nested_component)
            else:
                existing_labels[label] = nested_component

        if duplicate_labels_components:
            return OneComponentPerLabelAllowedRuleException(duplicate_labels_components)


class UnmatchedParameterKeyRuleException(RuleException):
    def __init__(self, unmatched_params: dict):
        self.unmatched_params = unmatched_params

    def __str__(self):
        return f"The following parameters do not have an implementation in the field they are trying to be initialized in  -> {self.unmatched_params}"


class UnmatchedParameterKeyRule(Rule):

    def validate(self, component: "ConfigurableComponentManager", monkey_cls) -> Union[RuleException, None]:
        unmatched_params = {}

        for param_key, param_val in component._init_params.items():
            if component.__parameters_components__:
                for parameter in component.__parameters_components__:
                    if param_key == parameter.__key__:
                        break
                    if parameter == component.__parameters_components__[-1]:
                        unmatched_params[param_key] = param_val
            else:
                # No parameters exist for the given component, so every given configuration is a mistake
                unmatched_params[param_key] = param_val

        if unmatched_params:
            return UnmatchedParameterKeyRuleException(unmatched_params)


class ConfigurableComponent(Component[TComponent], ABC, Generic[TComponent]):
    __rules__: ClassVar[Rules] = Rules([OneComponentPerLabelAllowedRule(), UnmatchedParameterKeyRule()])
    __parameters_components__: List[Type[TParameter]] = []

    @classmethod
    def parameter(cls, parameter: Type[TParameter]):
        """
        A decorator to add parameters into the current cls __parameters_components__ attr

            - overrides according to key.
            - allows priority inserting levels.
        """

        added = False
        cls.__parameters_components__ = list(cls.__parameters_components__)

        for i in range(len(cls.__parameters_components__)):
            exisisting_param = cls.__parameters_components__[i]
            if parameter.__key__ == exisisting_param.__key__:
                cls.__parameters_components__[i] = parameter
                added = True

        if not added:
            cls.__parameters_components__.append(parameter)

        return parameter

    def __init_subclass__(cls, copy_parameter_components=True):
        """
        copy_parameter_components -> False ->
            - will keep the same list memory context as the current Component cls itself.
            - if in the inheriting cls you override some parameter component so the same will happen to all base
              classes with the same memory dict.
        """

        if copy_parameter_components:
            cls.__parameters_components__ = cls.__parameters_components__.copy()

    def __init__(self, **params):
        self._init_params = params
        self._initialized_params: List[Parameter] = []
        self.__initiate_params(params)

    def __initiate_params(self, params: dict):
        for param_key, param_val in params.items():
            for possible_param in self.__parameters_components__:
                if param_key == possible_param.__key__:
                    self._initialized_params.append(possible_param(param_val))
                    break

    def _components(self, monkey_cls) -> List[Parameter]:
        return self._initialized_params
