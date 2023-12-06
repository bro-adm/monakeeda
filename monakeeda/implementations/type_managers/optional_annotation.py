from typing import Optional, Any

from monakeeda.base import annotation_mapper, ExceptionsDict
from monakeeda.consts import NamespacesConsts, FieldConsts
from .base_type_manager_annotation import BaseTypeManagerAnnotation
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor


@annotation_mapper(Optional)
class OptionalAnnotation(BaseTypeManagerAnnotation):
    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        if self._field_key in values:
            for component in self.managing:
                component.actuator = self
                model_instance.__run_organized_components__[component] = True

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        super()._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.REQUIRED] = False

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_optional_annotation(self, context)
