from typing import Tuple, Union, Any, Generic, T

from monakeeda.base import ExceptionsDict, OperatorVisitor, managed_by
from .base_numeric_constraint import NumericConstraintAnnotation
from .exceptions import NumericConstraintFailedException
from .lte_constraint import LTENumericConstraintFieldParameter
from ..general_annotations import NumericTypeAnnotation


@managed_by(NumericTypeAnnotation)
class Positive(NumericConstraintAnnotation[T], Generic[T]):
    __prior_handler__ = LTENumericConstraintFieldParameter

    @property
    def constraint(self) -> Tuple[str, Union[int, float]]:
        return 'gt', 0

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        value = values[self.scope]

        if value <= 0:
            exceptions[self.scope].append(NumericConstraintFailedException(self.representor, value))

    def accept_operator(self, operator_visitor: OperatorVisitor, context: Any):
        pass

