from typing import Generic, T, Any

from monakeeda.base import GenericAnnotation, Config
from monakeeda.consts import NamespacesConsts
from .exceptions import AbstractFieldFoundError
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor


class Abstract(GenericAnnotation, Generic[T]):
    __prior_handler__ = Config

    def _handle_values(self, model_instance, values, stage):
        getattr(model_instance, NamespacesConsts.EXCEPTIONS).append(AbstractFieldFoundError(self._field_key))

    def _act_with_value(self, value, cls, current_field_info, stage):
        pass

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_abstract_annotation(self, context)
