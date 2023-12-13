from abc import ABC
from typing import Any

from monakeeda.base import Annotation, annotation_mapper, type_validation, ExceptionsDict
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..type_managers import KnownLabels


class BasicTypeValidatorAnnotation(Annotation, ABC):
    __prior_handler__ = KnownLabels.TYPE_MANAGER

    @classmethod
    @property
    def label(cls) -> str:
        return "type_validator"


@annotation_mapper(object, Any)
class ObjectAnnotation(BasicTypeValidatorAnnotation):
    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        pass

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_object_annotation(self, context)


@annotation_mapper(str, list, dict)
class BasicTypeAnnotation(BasicTypeValidatorAnnotation):
    __prior_handler__ = KnownLabels.TYPE_MANAGER

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        result = type_validation(values[self._field_key], self.set_annotation)

        if result:
            exceptions[self.scope].append(result)
        else:
            for component in self.managing:
                component.actuators.add(self)
                model_instance.__run_organized_components__[component] = True

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_basic_annotation(self, context)


@annotation_mapper(int, float)
class NumericTypeAnnotation(BasicTypeAnnotation):
    __prior_handler__ = KnownLabels.TYPE_MANAGER
