from collections import defaultdict
from functools import lru_cache
from typing import Tuple, Any, Dict, List, Set

from monakeeda.base import annotation_mapper, ExceptionsDict, ComponentDecorator, Component, GenericAnnotation, \
    Annotation, get_all_managed_components
from .base_type_manager_annotation import BaseTypeManagerAnnotation
from ..existence_managers.exceptions import MissingFieldValueException
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor


class TupleComponentDecorator(ComponentDecorator):
    def __init__(self, main_tuple_annotation: 'TupleAnnotation'):
        super().__init__()
        self._main_tuple_annotation = main_tuple_annotation
        self.components_to_indices_mapping = defaultdict(lambda: set(), {})
        self.managers_activations_per_index: Dict[int, Dict[Component, List[Component]]] = defaultdict(lambda: {}, {})
        self.exceptions_per_index: Dict[int, List[Exception]] = defaultdict(lambda: [], {})

    def reset(self):
        self.managers_activations_per_index = defaultdict(lambda: {}, {})

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        for managing_component in self.actual_component.managers:
            if managing_component == self._main_tuple_annotation:
                if isinstance(self.actual_component, Annotation):
                    for index, annotations in self._main_tuple_annotation.annotations_per_item.items():
                        if self.actual_component in annotations:
                            self.components_to_indices_mapping[self.actual_component].add(index)
                            break
                else:
                    self.components_to_indices_mapping[self.actual_component] = set(range(len(self._main_tuple_annotation.direct_annotations)))
            else:
                self.components_to_indices_mapping[self.actual_component].update(self.components_to_indices_mapping[managing_component])

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        relevant_indices = self.components_to_indices_mapping[self.actual_component]
        field_key = self.actual_component._field_key
        tuple_value = list(values[field_key])

        for i in relevant_indices:
            item_activation_info = self.managers_activations_per_index[i]

            is_activated = False

            if self.component_actuator in item_activation_info:
                manager_activation_info = item_activation_info[self.component_actuator]
                if self.actual_component in manager_activation_info:
                    is_activated = True

            if is_activated:
                pre_run_activations = model_instance.__run_organized_components__.copy()

                item = tuple_value[i]
                values[field_key] = item

                relevant_exceptions = self.exceptions_per_index[i]
                relevant_exceptions_dict = ExceptionsDict()
                relevant_exceptions_dict[field_key] = relevant_exceptions
                self.component.handle_values(model_instance, values, stage, relevant_exceptions_dict)

                processed_value = values[field_key]
                tuple_value[i] = processed_value

                new_exceptions = set(relevant_exceptions) - set(exceptions[field_key])
                self.exceptions_per_index[i].extend(new_exceptions)
                exceptions[field_key].extend(new_exceptions)

                self.managers_activations_per_index[i][self.actual_component] = [component for component in self.actual_component.managing if model_instance.__run_organized_components__[component]]
                model_instance.__run_organized_components__ = pre_run_activations

        values[field_key] = tuple(tuple_value)


@annotation_mapper(Tuple)
class TupleAnnotation(BaseTypeManagerAnnotation):
    @property
    def represented_types(self):
        return tuple

    @property
    @lru_cache()
    def annotations_per_item(self) -> Dict[int, List[Annotation]]:
        annotations_per_index = {}
        for i in range(len(self.direct_annotations)):
            item_annotations = []

            direct_component = self.direct_annotations[i]
            item_annotations.append(direct_component)
            if isinstance(direct_component, GenericAnnotation):
                item_annotations.extend(direct_component.represented_annotations)

            annotations_per_index[i] = item_annotations

        return annotations_per_index

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        self.decorator = TupleComponentDecorator(self)
        super()._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        self.decorator.reset()

        value = values[self._field_key]
        relevant_activations = self.managing.copy()

        if not isinstance(value, self.represented_types):
            exceptions[self.scope].append(TypeError(f'Required to be provided with value of type {self.represented_types} -> but was provided with {type(value)}'))
        elif not len(value) == len(self.direct_annotations):
            exceptions[self.scope].append(ValueError(f'Required to be provided a {self.represented_types} of length {len(self.direct_annotations)} -> but was provided with {value} of len {len(value)}'))

            for i in range(len(value), len(self.direct_annotations)):
                self.decorator.exceptions_per_index[i] = [MissingFieldValueException()]

                for annotation in self.annotations_per_item[i]:
                    if annotation in relevant_activations:
                        relevant_activations.remove(annotation)

        for component in relevant_activations:
            relevant_indices = self.decorator.components_to_indices_mapping[component]
            component.actuators.append(self)
            model_instance.__run_organized_components__[component] = True

            for index in relevant_indices:
                self.decorator.managers_activations_per_index[index].setdefault(self, []).append(component)

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_list_annotation(self, context)
