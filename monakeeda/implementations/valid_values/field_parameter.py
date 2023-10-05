from typing import Any

from monakeeda.base import FieldParameter, Rules, Field
from ..rules import BasicParameterValueTypeValidationRule
from ..const import AllowMutation
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor


class NotAValidValue(ValueError):
    def __init__(self, valid_values, value_given):
        super(NotAValidValue, self).__init__(
            f"Valid values = {valid_values}. Value given = {value_given}")


@Field.parameter
class ValidValues(FieldParameter):
    __key__ = 'valid_values'
    __label__ = 'specific_value'
    __rules__ = Rules([BasicParameterValueTypeValidationRule((list, tuple, set))])
    __prior_handler__ = AllowMutation

    def handle_values(self, model_instance, values, stage) -> dict:
        val = values[self._field_key]

        if val not in self.param_val:
            raise NotAValidValue(self.param_val, val)

        return values

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_valid_values_field_parameter(self, context)
