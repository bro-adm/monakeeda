from typing import Any

from monakeeda.base import Annotation, annotation_mapper, type_validation, ExceptionsDict
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..type_managers import DictAnnotation


@annotation_mapper(object, Any)
class ObjectAnnotation(Annotation):
    __prior_handler__ = DictAnnotation

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        pass

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_object_annotation(self, context)


@annotation_mapper(int, str, list, dict)
class BasicTypeAnnotation(Annotation):
    __prior_handler__ = ObjectAnnotation

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        result = type_validation(values[self.scope], self.base_type)

        if result:
            exceptions[self.scope].append(result)

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_basic_annotation(self, context)
