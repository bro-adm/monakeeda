from typing import Generic, T, Any

from monakeeda.base import GenericAnnotation, Stages
from monakeeda.consts import NamespacesConsts
from .exceptions import ConstError
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..validators import Validator


class Const(GenericAnnotation, Generic[T]):
    __prior_handler__ = Validator

    def _handle_values(self, model_instance, values, stage):
        value = values[self._field_key]

        if stage == Stages.INIT:
            self._annotations[0].handle_values(model_instance, values, stage)

        elif stage == Stages.UPDATE:
            curr_val = getattr(model_instance, self._field_key)

            if value != curr_val:
                getattr(model_instance, NamespacesConsts.EXCEPTIONS).append(ConstError(curr_val, value))

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_const_annotation(self, context)