from typing import Optional, Any

from monakeeda.base import annotation_mapper, GenericAnnotation
from monakeeda.consts import NamespacesConsts, FieldConsts
from monakeeda.helpers import ExceptionsDict
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..values import DefaultFactoryFieldParameter


@annotation_mapper(Optional)
class OptionalAnnotation(GenericAnnotation):
    __prior_handler__ = DefaultFactoryFieldParameter

    def _handle_values(self, model_instance, values, stage):
        if self._field_key in values:
            self._annotations[0].handle_values(model_instance, values, stage)

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        super()._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.REQUIRED] = False

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_optional_annotation(self, context)
