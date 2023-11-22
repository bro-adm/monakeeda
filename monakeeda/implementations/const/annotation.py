from typing import Generic, T, Any

from monakeeda.base import GenericAnnotation, Stages, ExceptionsDict
from monakeeda.consts import NamespacesConsts
from .exceptions import ConstError
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..validators import Validator


class Const(GenericAnnotation, Generic[T]):
    __prior_handler__ = Validator

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        if stage == Stages.INIT:
            self._annotations[0].handle_values(model_instance, values, stage, exceptions)

        elif stage == Stages.UPDATE:
            curr_val = getattr(model_instance, self._field_key)
            self._annotations[0].handle_values(model_instance, values, stage, exceptions)

            value = values[self._field_key]

            if value != curr_val:
                exceptions[self.scope].append(ConstError(curr_val, value))

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_const_annotation(self, context)