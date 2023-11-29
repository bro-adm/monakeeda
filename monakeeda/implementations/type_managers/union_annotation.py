from typing import Union, Any

from monakeeda.base import annotation_mapper, GenericAnnotation, ExceptionsDict, type_validation
from ..existence_managers import CreateFrom
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor


@annotation_mapper(Union)
class UnionAnnotation(GenericAnnotation):
    __prior_handler__ = CreateFrom

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        union_types = self.args

        result = type_validation(values[self.scope], union_types)

        if result:
            exceptions[self.scope].append(result)

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_union_annotation(self, context)
