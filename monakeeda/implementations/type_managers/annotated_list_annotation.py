from typing import List, Any

from monakeeda.base import annotation_mapper, GenericAnnotation, ExceptionsDict
from .discriminator_annotation import Discriminator
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor


@annotation_mapper(List)
class ListAnnotation(GenericAnnotation):
    __prior_handler__ = Discriminator

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        value = values[self.scope]

        list_type = self.args
        unmatched_values = []

        for val in value:
            if not isinstance(val, list_type):
                unmatched_values.append(value)

        if unmatched_values:
            exceptions[self.scope].append(
                TypeError(f'the following values are not of type {list_type} -> {unmatched_values}'))

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_list_annotation(self, context)
