from typing import Any

from monakeeda.base import FieldParameter, Field, ExceptionsDict, managed_by
from ..type_managers import OptionalAnnotation
from ..numeric_constraints import NumericConstraintFieldParameter
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..known_builders import ParameterValueTypeValidator


@managed_by(OptionalAnnotation)
@Field.parameter
class ValidValues(FieldParameter):
    __key__ = 'valid_values'
    __builders__ = [ParameterValueTypeValidator((list, tuple, set))]
    __prior_handler__ = NumericConstraintFieldParameter.label

    @classmethod
    @property
    def label(cls) -> str:
        return "validations"

    def is_collision(self, other) -> bool:
        super().is_collision(other)
        return False

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        val = values[self._field_key]

        if val not in self.param_val:
            exceptions[self.scope].append(ValueError(f"{self.representor} = {self.param_val}, received {val}"))

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_valid_values_field_parameter(self, context)
