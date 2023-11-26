from typing import Any

from monakeeda.base import Field, ExceptionsDict
from .base_numeric_constraint import NumericConstraintFieldParameter
from .exceptions import NumericConstraintFailedException
from .gte_constraint import GTENumericConstraintFieldParameter
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor


@Field.parameter
class LTNumericConstraintFieldParameter(NumericConstraintFieldParameter):
    __key__ = "lt"
    __prior_handler__ = GTENumericConstraintFieldParameter

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        value = values[self.scope]

        if value >= self.param_val:
            exceptions[self.scope].append(NumericConstraintFailedException(f"{self.representor}={self.param_val}", value))

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        pass
