from typing import Any

from monakeeda.base import Field, ExceptionsDict
from .base_numeric_constraint import NumericConstraintFieldParameter
from .exceptions import NumericConstraintFailedException
from .gt_constraint import GTNumericConstraintFieldParameter
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor


@Field.parameter
class GTENumericConstraintFieldParameter(NumericConstraintFieldParameter):
    __key__ = "gte"
    __prior_handler__ = GTNumericConstraintFieldParameter

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        value = values[self.scope]

        if value < self.param_val:
            exceptions[self.scope].append(NumericConstraintFailedException(f"{self.representor}={self.param_val}", value))

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        pass
