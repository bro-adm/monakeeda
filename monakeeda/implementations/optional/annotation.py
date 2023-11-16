from typing import Optional, Any

from monakeeda.base import annotation_mapper, GenericAnnotation, get_generics_annotations
from monakeeda.consts import NamespacesConsts, FieldConsts
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..values import DefaultFactoryFieldParameter


@annotation_mapper(Optional)
class OptionalAnnotation(GenericAnnotation):
    __prior_handler__ = DefaultFactoryFieldParameter

    def _handle_values(self, model_instance, values, stage):
        if self._field_key in values:
            get_generics_annotations(self)[0].handle_values(model_instance, values, stage)

    def build(self, monkey_cls, bases, monkey_attrs):
        super().build(monkey_cls, bases, monkey_attrs)
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.REQUIRED] = False

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_optional_annotation(self, context)
