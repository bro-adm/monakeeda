from typing import Any

from monakeeda.base import Field, ExceptionsDict, managed_by
from .base_numeric_constraint import NumericConstraintFieldParameter
from .exceptions import NumericConstraintFailedException
from .negative_annotation import Negative
from .positive_annotation import Positive
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..type_validators import NumericTypeAnnotation


@managed_by(NumericTypeAnnotation, Positive, Negative)
@Field.parameter
class LTENumericConstraintFieldParameter(NumericConstraintFieldParameter):
    __key__ = "lte"

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        value = values[self.scope]

        if value > self.param_val:
            exceptions[self.scope].append(NumericConstraintFailedException(f"{self.representor}={self.param_val}", value))

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        pass
