from typing import Any

from monakeeda.base import Field, ExceptionsDict, managed_by
from .base_numeric_constraint import NumericConstraintFieldParameter
from .exceptions import NumericConstraintFailedException
from ..general_annotations import NumericTypeAnnotation
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..valid_values import ValidValues


@managed_by(NumericTypeAnnotation)
@Field.parameter
class GTNumericConstraintFieldParameter(NumericConstraintFieldParameter):
    __key__ = "gt"
    __prior_handler__ = ValidValues

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        value = values[self.scope]

        if value <= self.param_val:
            exceptions[self.scope].append(
                NumericConstraintFailedException(f"{self.representor}={self.param_val}", value))

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        pass
