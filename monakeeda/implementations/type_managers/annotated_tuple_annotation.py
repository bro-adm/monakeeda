from collections import defaultdict
from typing import Tuple, Any, Dict, List

from monakeeda.base import annotation_mapper, ExceptionsDict, ComponentDecorator, Component, GenericAnnotation, \
    Annotation, get_all_managed_components
from .base_type_manager_annotation import BaseTypeManagerAnnotation
from ..existence_managers.exceptions import MissingFieldValueException
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor


class TupleComponentDecorator(ComponentDecorator):
    def __init__(self, managers_indices_mapping: Dict[Component, List[int]]):
        super().__init__()
        self.components_to_indices_mapping = managers_indices_mapping
        self.managers_activations_per_index: Dict[int, Dict[Component, List[Component]]] = defaultdict(lambda: {}, {})
        self.exceptions_per_index: Dict[int, List[Exception]] = defaultdict(lambda: [], {})

    def reset(self):
        self.managers_activations_per_index = defaultdict(lambda: {}, {})

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        relevant_indices = self.components_to_indices_mapping[self.component]
        field_key = self.component._field_key
        tuple_value = list(values[field_key])

        for i in relevant_indices:
            item_activation_info = self.managers_activations_per_index[i]

            is_activated = False

            for manager in self.component.managers:
                if manager in item_activation_info:
                    manager_activation_info = item_activation_info[manager]
                    if self.component in manager_activation_info:
                        is_activated = True
                        break

            if is_activated:
                pre_run_activations = model_instance.__run_organized_components__.copy()

                item = tuple_value[i]
                values[field_key] = item

                relevant_exceptions = self.exceptions_per_index[item]
                relevant_exceptions_dict = ExceptionsDict()
                relevant_exceptions_dict[field_key] = relevant_exceptions
                self.component.handle_values(model_instance, values, stage, relevant_exceptions_dict)

                processed_value = values[field_key]
                tuple_value[i] = processed_value

                new_exceptions = set(relevant_exceptions) - set(exceptions[field_key])
                self.exceptions_per_index[item].extend(new_exceptions)
                exceptions[field_key].extend(new_exceptions)

                self.managers_activations_per_index[i][self.component] = [component for component in self.component.managing if model_instance.__run_organized_components__[component]]
                model_instance.__run_organized_components__ = pre_run_activations

        values[field_key] = tuple(tuple_value)


@annotation_mapper(Tuple)
class TupleAnnotation(BaseTypeManagerAnnotation):
    @property
    def represented_types(self):
        return tuple

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        i = 0
        managed_indices_map = defaultdict(lambda: [], {})
        for component in self.direct_annotations:
            managed_indices_map[component] = [i]
            if isinstance(component, GenericAnnotation):
                for sub_component in component.represented_annotations:
                    managed_indices_map[sub_component] = [i]
            # TODO: add build logic to decorator and let managed components run those builds after they know who they mnage
            i += 1

        self.decorator = TupleComponentDecorator(managed_indices_map)
        super()._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)

        for component in self.managing:
            if not isinstance(component, Annotation):
                self.decorator.components_to_indices_mapping[component] = list(range(len(self.direct_annotations)))

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        self.decorator.reset()

        value = values[self._field_key]
        relevant_activations = self.managing.copy()

        if not isinstance(value, self.represented_types):
            exceptions[self.scope].append(
                TypeError(f'Required to be provided with value of type {self.represented_types} -> but was provided with {type(value)}'))
        elif not len(value) == len(self.direct_annotations):
            exceptions[self.scope].append(
                ValueError(f'Required to be provided a {self.represented_types} of length {len(self.direct_annotations)} -> but was provided with {value} of len {len(value)}'))

            for i in range(len(value), len(self.direct_annotations)):
                self.decorator.exceptions_per_index[i] = [MissingFieldValueException()]

            relevant_represented_annotations = self.direct_annotations[:len(value)]
            relevant_represented_annotations.extend([relevant_annotation.represented_annotations for relevant_annotation in relevant_represented_annotations if isinstance(relevant_annotation, GenericAnnotation)])

            for component in self.managing:
                if component not in relevant_represented_annotations and isinstance(component, Annotation):
                    relevant_activations.remove(component)
                    # If there are any non Annotation managed components that usually run on all items of the tuple ->
                    # They won't run on the problematic indices because of the inserted exceptions on those indices.
                    # NOTE: we do not want ot change the component's relavnt indices mapping at run time -> that is a build setup thing

        for component in relevant_activations:
            relevant_indices = self.decorator.components_to_indices_mapping[component]
            component.actuator = self
            model_instance.__run_organized_components__[component] = True

            for index in relevant_indices:
                self.decorator.managers_activations_per_index[index].setdefault(self, []).append(component)

            for managed_component in get_all_managed_components(component):
                self.decorator.components_to_indices_mapping[managed_component] = self.decorator.components_to_indices_mapping[component]

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_list_annotation(self, context)
