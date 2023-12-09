from collections import defaultdict
from typing import Tuple, Any, Dict, List

from monakeeda.base import annotation_mapper, ExceptionsDict, ComponentDecorator, Component, GenericAnnotation, \
    Annotation, get_all_managed_components
from monakeeda.utils import list_insert_if_does_not_exist
from .base_type_manager_annotation import BaseTypeManagerAnnotation
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..existence_managers.exceptions import MissingFieldValueException


class TupleComponentDecorator(ComponentDecorator):
    def __init__(self, managers_indices_mapping: Dict[Component, List[int]]):
        super().__init__()
        self.managers_indices_mapping = managers_indices_mapping
        self._activations_per_item: List[Dict[Component, Dict[Component, bool]]] = []
        self._exceptions_per_item: Dict[int, List[Exception]] = defaultdict(lambda: [], {})

    def reset(self):
        self._activations_per_item = []

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        relevant_indices = self.managers_indices_mapping[self.component]
        field_key = self.component._field_key
        tuple_value = list(values[field_key])

        for i in relevant_indices:
            item_activation_info = list_insert_if_does_not_exist(self._activations_per_item, i, {})

            is_activated = False

            if not item_activation_info:
                is_activated = True

            else:
                for manager in self.component.managers:
                    if manager in item_activation_info:
                        manager_activation_info = item_activation_info[manager]
                        if manager_activation_info[self.component]:
                            is_activated = True
                            break

            if is_activated:
                pre_run_activations = model_instance.__run_organized_components__.copy()

                item = tuple_value[i]
                values[field_key] = item

                relevant_exceptions = self._exceptions_per_item[item]
                relevant_exceptions_dict = ExceptionsDict()
                relevant_exceptions_dict[field_key] = relevant_exceptions
                self.component.handle_values(model_instance, values, stage, relevant_exceptions_dict)

                processed_value = values[field_key]
                tuple_value[i] = processed_value

                new_exceptions = set(relevant_exceptions) - set(exceptions[field_key])
                self._exceptions_per_item[item].extend(new_exceptions)
                exceptions[field_key].extend(new_exceptions)

                self._activations_per_item[i][self.component] = model_instance.__run_organized_components__.copy()
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
            managed_indices_map[component.main_annotation] = [i]
            # for managed_component in get_all_managed_components(component):
            #     managed_indices_map[managed_component].extend(managed_indices_map[component.main_annotation])

            i += 1

        self.decorator = TupleComponentDecorator(managed_indices_map)
        super()._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)

        for component in self.managing:
            if not isinstance(component, Annotation):
                self.decorator.managers_indices_mapping[component] = list(range(len(self.direct_annotations)))

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
                self.decorator._exceptions_per_item[i] = [MissingFieldValueException()]

            relevant_represented_annotations = self.direct_annotations[:len(value)]
            relevant_represented_annotations.extend([relevant_annotation.represented_annotations for relevant_annotation in relevant_represented_annotations if isinstance(relevant_annotation, GenericAnnotation)])

            for component in self.managing:
                if component not in relevant_represented_annotations and isinstance(component, Annotation):
                    relevant_activations.remove(component)
                    # If there are any non Annotation managed components that usually run on all items of the tuple ->
                    # They won't run on the problematic indices because of the inserted exceptions on those indices.
                    # NOTE: we do not want ot change the component's relavnt indices mapping at run time -> that is a build setup thing

        for component in relevant_activations:
            component.actuator = self
            model_instance.__run_organized_components__[component] = True

            for managed_component in get_all_managed_components(component):
                self.decorator.managers_indices_mapping[managed_component].extend(self.decorator.managers_indices_mapping[component])

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_list_annotation(self, context)
