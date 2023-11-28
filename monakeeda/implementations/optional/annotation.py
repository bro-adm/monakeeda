from typing import Optional, Any

from monakeeda.base import annotation_mapper, GenericAnnotation, ExceptionsDict
from monakeeda.consts import NamespacesConsts, FieldConsts
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..value_providers import ValueFieldParameter


@annotation_mapper(Optional)
class OptionalAnnotation(GenericAnnotation):
    __prior_handler__ = ValueFieldParameter

    @classmethod
    @property
    def label(cls) -> str:
        return "requirement_manager"

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        if self._field_key in values:
            self._annotations[0].handle_values(model_instance, values, stage, exceptions)

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        super()._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.REQUIRED] = False

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_optional_annotation(self, context)
