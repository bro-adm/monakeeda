from collections import defaultdict
from typing import List, Any, Dict

from monakeeda.base import annotation_mapper, ExceptionsDict, ComponentDecorator, Component
from monakeeda.utils import list_insert_if_does_not_exist
from .base_type_manager_annotation import BaseTypeManagerAnnotation
from .consts import KnownLabels
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor


class ListComponentDecorator(ComponentDecorator):
    def __init__(self):
        super().__init__()
        self._activations_per_item: List[Dict[Component, Dict[Component, bool]]] = []
        self._exceptions_per_item: Dict[int, List[Exception]] = defaultdict(lambda: [], {})

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        field_key = self.component._field_key
        list_value = values[field_key]

        for i in range(len(list_value)):
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

                item = list_value[i]
                values[field_key] = item

                relevant_exceptions = self._exceptions_per_item[item]
                relevant_exceptions_dict = ExceptionsDict()
                relevant_exceptions_dict[field_key] = relevant_exceptions
                self.component.handle_values(model_instance, values, stage, relevant_exceptions_dict)

                processed_value = values[field_key]
                list_value[i] = processed_value

                new_exceptions = set(relevant_exceptions) - set(exceptions[field_key])
                self._exceptions_per_item[item].extend(new_exceptions)
                exceptions[field_key].extend(new_exceptions)

                self._activations_per_item[i][self.component] = model_instance.__run_organized_components__.copy()
                model_instance.__run_organized_components__ = pre_run_activations
                print(model_instance.__run_organized_components__)

        values[field_key] = list_value


@annotation_mapper(List)
class ListAnnotation(BaseTypeManagerAnnotation):
    @property
    def represented_types(self):
        return list

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        self.decorator = ListComponentDecorator()
        super()._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        value = values[self._field_key]

        if isinstance(value, list):
            for component in self.managing:
                component.actuator = self
                model_instance.__run_organized_components__[component] = True

        else:
            exceptions[self.scope].append(TypeError(f'Required to be provided with value of type list -> but was provided with {type(value)}'))

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_list_annotation(self, context)
