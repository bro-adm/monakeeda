from typing import Tuple, Union, Any, Generic, T

from monakeeda.base import ExceptionsDict, OperatorVisitor, managed_by
from .base_numeric_constraint import NumericConstraintAnnotation
from .exceptions import NumericConstraintFailedException
from ..general_annotations import NumericTypeAnnotation
from ..valid_values import ValidValues


@managed_by(NumericTypeAnnotation)
class Positive(NumericConstraintAnnotation[T], Generic[T]):
    __prior_handler__ = ValidValues

    def __instancecheck__(self, instance):
        if isinstance(instance, self.args):
            return instance > 0

        return False

    @property
    def constraint(self) -> Tuple[str, Union[int, float]]:
        return 'gt', 0

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        value = values[self.scope]

        if value <= 0:
            exceptions[self.scope].append(NumericConstraintFailedException(self.representor, value))
        else:
            for component in self.managing:
                component.actuator = self
                model_instance.__run_organized_components__[component] = True

    def accept_operator(self, operator_visitor: OperatorVisitor, context: Any):
        pass
