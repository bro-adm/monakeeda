from typing import Any

from monakeeda.base import Field, ExceptionsDict
from .base_numeric_constraint import NumericConstraintFieldParameter
from .exceptions import NumericConstraintFailedException
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..valid_values import ValidValues


@Field.parameter
class GTNumericConstraintFieldParameter(NumericConstraintFieldParameter):
    __key__ = "gt"
    __prior_handler__ = ValidValues

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        value = values[self.scope]

        if value <= self.param_val:
            exceptions[self.scope].append(NumericConstraintFailedException(self, self.param_val, value))

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        pass
