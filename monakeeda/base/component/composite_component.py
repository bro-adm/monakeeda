from abc import ABC, abstractmethod
from typing import List, Generic, Dict, Union

from .component import TComponent, Component
from .rules import RuleException, Rule


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

    def validate(self, component: "BaseComponentComposite") -> Union[RuleException, None]:
        existing_labels: Dict[str, Component] = {}
        duplicate_labels_components: Dict[str, List[Component]] = {}

        for nested_component in component._components:
            label = nested_component.__label__
            if label in existing_labels:
                duplicate_labels_components.setdefault(label, [existing_labels[label]])
                duplicate_labels_components[label].append(nested_component)
            else:
                existing_labels[label] = nested_component

        if duplicate_labels_components:
            return OneComponentPerLabelAllowedRuleException(duplicate_labels_components)


class BaseComponentComposite(Component, Generic[TComponent], ABC):
    """
    Composite DP implementation.

    The components list is not available always via init.
    So this is an ABC implementation with all additional components listing discovery methods
    being custom one level inheritance implementations.
    """

    @property
    @abstractmethod
    def _components(self) -> List[TComponent]:
        pass

    def values_handler(self, key, model_instance, values) -> dict:
        calculated_values = values
        for component in self._components:
            calculated_values = component.values_handler(key, model_instance, calculated_values)

        return calculated_values

    def _set_cls_landscape(self, monkey_cls, bases, monkey_attrs):
        # TODO: decide if to make this method not abstract with this nothing implementation

        pass

    def build(self, monkey_cls, bases, monkey_attrs) -> bool:
        is_valid = True

        for component in self._components:
            # Keeps is_valid False if was False, else runs next components build (for additional errors and setups)
            is_valid = is_valid if not is_valid else component.build(monkey_cls, bases, monkey_attrs)

        return is_valid


class ComponentInitComposite(BaseComponentComposite, Generic[TComponent]):
    def __init__(self, components: List[TComponent]):
        self._init_components = components

    @property
    def _components(self) -> List[TComponent]:
        return self._init_components
