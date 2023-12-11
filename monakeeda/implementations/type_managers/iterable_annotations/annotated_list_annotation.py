from collections import defaultdict
from typing import List, Any, Dict

from monakeeda.base import annotation_mapper, ExceptionsDict, ComponentDecorator, Component
from .errors import ItemException
from ..base_type_manager_annotation import BaseTypeManagerAnnotation
from ...implemenations_base_operator_visitor import ImplementationsOperatorVisitor


class ListComponentDecorator(ComponentDecorator['ListAnnotation']):
    def __init__(self, decorating_component: 'ListAnnotation'):
        super().__init__(decorating_component)
        self.managers_activations_per_index: Dict[int, Dict[Component, List[Component]]] = defaultdict(lambda: {}, {})
        self.exceptions_per_index: Dict[int, List[Exception]] = defaultdict(lambda: [], {})

    def reset(self):
        self.managers_activations_per_index = defaultdict(lambda: {}, {})

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        pass
        
    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        field_key = self.actual_component._field_key
        list_value = values[field_key]

        for i in range(len(list_value)):
            item_activation_info = self.managers_activations_per_index[i]

            is_activated = False

            if self.direct_decorator_component in item_activation_info and self.actual_component in item_activation_info[self.direct_decorator_component]:
                is_activated = True
            elif self.component_actuator in item_activation_info:
                manager_activation_info = item_activation_info[self.component_actuator]
                if self.actual_component in manager_activation_info:
                    is_activated = True

            if is_activated:
                pre_run_activations = model_instance.__run_organized_components__.copy()

                item = list_value[i]
                values[field_key] = item

                relevant_exceptions = self.exceptions_per_index[i]
                relevant_exceptions_dict = ExceptionsDict()
                relevant_exceptions_dict[field_key] = relevant_exceptions
                self.component.handle_values(model_instance, values, stage, relevant_exceptions_dict)

                processed_value = values[field_key]
                list_value[i] = processed_value

                new_exceptions = set(relevant_exceptions) - set(exceptions[field_key])
                new_exceptions = [ItemException(self._decorating_component.represented_types, i, exception) for exception in new_exceptions]
                self.exceptions_per_index[i].extend(new_exceptions)
                exceptions[field_key].extend(new_exceptions)

                self.managers_activations_per_index[i][self.component] = model_instance.__run_organized_components__.copy()
                model_instance.__run_organized_components__ = pre_run_activations

        values[field_key] = list_value


@annotation_mapper(List)
class ListAnnotation(BaseTypeManagerAnnotation):
    @property
    def represented_types(self):
        return list

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        self.decorator = ListComponentDecorator(self)
        super()._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        value = values[self._field_key]

        if isinstance(value, list):
            for component in self.managing:
                component.actuators.append(self)
                model_instance.__run_organized_components__[component] = True

                for i in range(len(value)):
                    self.decorator.managers_activations_per_index[i].setdefault(self, []).append(component)

        else:
            exceptions[self.scope].append(TypeError(f'Required to be provided with value of type list -> but was provided with {type(value)}'))

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_list_annotation(self, context)
