from collections import defaultdict
from enum import Enum
from functools import lru_cache
from typing import Dict, Any, TypedDict, Generic, TypeVar, List, Set

from monakeeda.base import annotation_mapper, ExceptionsDict, OperatorVisitor, ComponentDecorator, Annotation, \
    GenericAnnotation, Component
from .errors import ItemException
from ..base_type_manager_annotation import BaseTypeManagerAnnotation

TInfo = TypeVar('TInfo')


class DictCompartments(Enum):
    key = 'key'
    value = 'value'


class DictCompartmentsInfo(TypedDict, Generic[TInfo]):
    key: TInfo
    value: TInfo


# Wish python would have a SimpleConsts class or something like that also was used as a tuple :(
dict_compartments = dict(DictCompartmentsInfo(key=DictCompartments.key, value=DictCompartments.value))


class DictComponentDecorator(ComponentDecorator['DictAnnotation']):

    def __init__(self, decorating_component: 'DictAnnotation'):
        super().__init__(decorating_component)
        self.components_to_dict_compartments_mapping: Dict[Component, Set[DictCompartments]] = defaultdict(lambda: set(), {})
        self.managers_activations_per_dict_compartment = DictCompartmentsInfo[Dict[int, Dict[Component, List[Component]]]](key=defaultdict(lambda: {}, {}), value=defaultdict(lambda: {}, {}))
        self.exceptions_per_dict_compartment = DictCompartmentsInfo[Dict[int, List[Exception]]](key=defaultdict(lambda: [], {}), value=defaultdict(lambda: [], {}))

    def reset(self):
        self.managers_activations_per_dict_compartment = DictCompartmentsInfo[Dict[int, Dict[Component, List[Component]]]](key=defaultdict(lambda: {}, {}), value=defaultdict(lambda: {}, {}))
        self.exceptions_per_dict_compartment = DictCompartmentsInfo[Dict[int, List[Exception]]](key=defaultdict(lambda: [], {}), value=defaultdict(lambda: [], {}))

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        for managing_component in self.component.managers:
            if managing_component == self._decorating_component:
                if isinstance(self.component, Annotation):
                    for dict_compartment, annotations in self._decorating_component.annotations_per_dict_compartment.items():
                        if self.component in annotations:
                            self.components_to_dict_compartments_mapping[self.component].add(dict_compartments[dict_compartment])
                            break
                else:
                    # DOnt know what such a component would be :|
                    self.components_to_dict_compartments_mapping[self.component] = {DictCompartments.key, DictCompartments.value}
            else:
                self.components_to_dict_compartments_mapping[self.component].update(self.components_to_dict_compartments_mapping[managing_component])

    def _extract_compartment(self, original_value: dict, compartment: DictCompartments) -> List[Any]:
        if compartment == DictCompartments.key:
            return list(original_value.keys())
        elif compartment == DictCompartments.value:
            return list(original_value.values())

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        relevant_dict_compartments = self.components_to_dict_compartments_mapping[self.component]
        field_key = self.component._field_key
        dict_value = values[field_key]

        dict_keys = dict_value.keys()
        dict_values = dict_value.values()

        print(f"--- Start Dict Decorator {relevant_dict_compartments} ---")

        for compartment in relevant_dict_compartments:
            compartment_items = self._extract_compartment(dict_value, compartment)
            compartment_activation_info = self.managers_activations_per_dict_compartment[compartment.value]
            compartment_exceptions = self.exceptions_per_dict_compartment[compartment.value]

            if compartment == DictCompartments.key:
                dict_keys = compartment_items
            elif compartment == DictCompartments.value:
                dict_values = compartment_items

            for i in range(len(compartment_items)):
                item_activation_info = compartment_activation_info[i]

                is_activated = False

                print(f"{self.decorated=}, {self.direct_decorator_component=}, {i=}, {item_activation_info=}")

                if isinstance(self.decorated, ComponentDecorator):
                    print(f"{self.decorated._decorating_component=}")
                    if self.decorated._decorating_component in item_activation_info:
                        if item_activation_info[self.decorated._decorating_component]:
                            is_activated = True

                if self.component_actuator in item_activation_info:
                    manager_activation_info = item_activation_info[self.component_actuator]
                    if self.component in manager_activation_info:
                        is_activated = True

                print(f"{is_activated=}")

                if is_activated:
                    pre_run_activations = model_instance.__run_organized_components__.copy()

                    item = compartment_items[i]
                    values[field_key] = item

                    relevant_exceptions = compartment_exceptions[i]
                    relevant_exceptions_dict = ExceptionsDict()
                    relevant_exceptions_dict[field_key] = relevant_exceptions
                    self.decorated.handle_values(model_instance, values, stage, relevant_exceptions_dict)

                    processed_value = values[field_key]
                    compartment_items[i] = processed_value

                    new_exceptions = set(relevant_exceptions) - set(exceptions[field_key])
                    print(f"{new_exceptions=}")
                    for exception in new_exceptions:
                        relevant_exceptions.remove(exception)
                        wrapped_exception = ItemException(self._decorating_component.represented_types, f"{compartment.value}-{i}", exception)
                        print(f"ADDED {wrapped_exception}, {self._decorating_component.representor}, {exceptions.__repr__()}")
                        exceptions[field_key].append(wrapped_exception)
                        relevant_exceptions.append(wrapped_exception)

                    compartment_activation_info[i][self.component] = [component for component in self.component.managing if model_instance.__run_organized_components__[component]]
                    print(f"new activations = {compartment_activation_info[i][self.component]}")
                    model_instance.__run_organized_components__ = pre_run_activations

        values[field_key] = {key: val for key, val in zip(dict_keys, dict_values)}
        print(f"--- End Dict Decorator {relevant_dict_compartments} ---")


@annotation_mapper(Dict)
class DictAnnotation(BaseTypeManagerAnnotation):

    @property
    def represented_types(self):
        return dict

    @property
    @lru_cache()
    def annotations_per_dict_compartment(self) -> DictCompartmentsInfo[List[Annotation]]:
        annotations_per_dict_compartment = {}
        key_annotation, value_annotation = self.direct_annotations

        def _inner(dict_compartment: DictCompartments, annotation: Annotation):
            compartment_annotations = [annotation]

            if isinstance(annotation, GenericAnnotation):
                compartment_annotations.extend(annotation.represented_annotations)

            annotations_per_dict_compartment[dict_compartment] = compartment_annotations

        _inner(DictCompartments.key.value, key_annotation)
        _inner(DictCompartments.value.value, value_annotation)

        return DictCompartmentsInfo[List[Annotation]](annotations_per_dict_compartment)

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        self.decorator = DictComponentDecorator(self)
        super()._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        self.decorator.reset()

        value = values[self._field_key]

        if isinstance(value, self.represented_types):
            for component in self.managing:
                component.actuators.add(self)
                model_instance.__run_organized_components__[component] = True

                for i in range(len(value)):
                    relevant_dict_compartments = self.decorator.components_to_dict_compartments_mapping[component]
                    for relevant_dict_compartment in relevant_dict_compartments:
                        self.decorator.managers_activations_per_dict_compartment[relevant_dict_compartment.value][i].setdefault(self, []).append(component)
        else:
            exceptions[self.scope].append(TypeError(f'Required to be provided with value of type {self.represented_types} -> but was provided with {type(value)}'))

    def accept_operator(self, operator_visitor: OperatorVisitor, context: Any):
        pass
