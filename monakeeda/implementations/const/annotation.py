from typing import Generic, T, Any

from monakeeda.base import GenericAnnotation, Stages, ExceptionsDict, managed_by
from .consts import MUTATION_MANAGER
from .exceptions import ConstError
from ..type_managers import OptionalAnnotation
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..mutators import Mutator
from ..type_managers import Discriminator, UnionAnnotation


@managed_by(OptionalAnnotation, Discriminator, UnionAnnotation)
class Const(GenericAnnotation, Generic[T]):
    __prior_handler__ = Mutator

    @classmethod
    @property
    def label(cls) -> str:
        return MUTATION_MANAGER

    @property
    def main_annotation(self):
        return self.direct_annotations[0].main_annotation

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        if stage == Stages.UPDATE:
            curr_val = getattr(model_instance, self._field_key)

            value = values[self._field_key]

            if value != curr_val:
                exceptions[self._field_key].append(ConstError(curr_val, value))

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_const_annotation(self, context)
