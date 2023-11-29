from typing import Generic, T, Any

from monakeeda.base import GenericAnnotation, Stages, ExceptionsDict
from .consts import MUTATION_MANAGER
from .exceptions import ConstError
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..mutators import Mutator


class Const(GenericAnnotation, Generic[T]):
    __prior_handler__ = Mutator

    @classmethod
    @property
    def label(cls) -> str:
        return MUTATION_MANAGER

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        if stage == Stages.INIT:
            self.represented_annotations[0].handle_values(model_instance, values, stage, exceptions)

        elif stage == Stages.UPDATE:
            curr_val = getattr(model_instance, self.scope)
            self.represented_annotations[0].handle_values(model_instance, values, stage, exceptions)

            value = values[self.scope]

            if value != curr_val:
                exceptions[self.scope].append(ConstError(curr_val, value))

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_const_annotation(self, context)