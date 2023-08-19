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

    def validate(self, component: "BaseComponentComposite", monkey_cls) -> Union[RuleException, None]:
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


class BaseComponentComposite(Component, Generic[TComponent], ABC):
    """
    Composite DP implementation.

    The components list is not available always via init.
    So this is an ABC implementation with all additional components listing discovery methods
    being custom one level inheritance implementations.
    """

    @abstractmethod
    def _components(self, monkey_cls) -> List[TComponent]:
        """
        Returns a list of the composite components under its management.

        components might reside under a namespace in the monkey_cls or in the components instance
        """

        pass

    def _values_handler(self, model_instance, values, stage) -> dict:
        for component in self._components(model_instance.__class__):
            calculated_values = component._values_handler(model_instance, values, stage)
            values.update(calculated_values)

        return values

    # TODO: Rethink the fact that _set_cls_landscape does not work on returns but currently via updates -> makes every step harder and requires more precise components -> example FieldsMainComponent, FieldParameter and Field(Configuarble)Component effected inits
    def _set_cls_landscape(self, monkey_cls, bases, monkey_attrs):
        for component in self._components(monkey_cls):
            component._set_cls_landscape(monkey_cls, bases, monkey_attrs)

    def build(self, monkey_cls, bases, monkey_attrs) -> bool:
        is_valid = True

        for component in self._components(monkey_cls):
            # Keeps is_valid False if was False, else runs next components build (for additional errors and setups)
            is_valid = is_valid if not is_valid else component.build(monkey_cls, bases, monkey_attrs)

        if is_valid:
            return super().build(monkey_cls, bases, monkey_attrs)

        return is_valid  # False
