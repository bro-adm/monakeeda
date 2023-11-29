from typing import Any

from monakeeda.base import Annotation, annotation_mapper, type_validation, ExceptionsDict, managed_by
from ..existence_managers import OptionalAnnotation
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..type_managers import DictAnnotation, UnionAnnotation


@managed_by(OptionalAnnotation, UnionAnnotation)
@annotation_mapper(object, Any)
class ObjectAnnotation(Annotation):
    __prior_handler__ = DictAnnotation

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        pass

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_object_annotation(self, context)


@managed_by(OptionalAnnotation, UnionAnnotation)
@annotation_mapper(str, list, dict)
class BasicTypeAnnotation(Annotation):
    __prior_handler__ = ObjectAnnotation

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        result = type_validation(values[self.scope], self.base_type)

        if result:
            exceptions[self.scope].append(result)
        else:
            for component in self.managing:
                model_instance.__run_organized_components__[component] = True

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_basic_annotation(self, context)


@managed_by(OptionalAnnotation, UnionAnnotation)
@annotation_mapper(int, float)
class NumericTypeAnnotation(BasicTypeAnnotation):
    __prior_handler__ = BasicTypeAnnotation
