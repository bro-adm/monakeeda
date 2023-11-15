from typing import Any

from monakeeda.base import FieldParameter, Rules, Field, ArbitraryAnnotation
from monakeeda.consts import NamespacesConsts
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..missing.errors import MissingFieldValuesException
from ..rules import BasicParameterValueTypeValidationRule


class NotAValidValue(ValueError):
    def __init__(self, valid_values, value_given):
        super(NotAValidValue, self).__init__(
            f"Valid values = {valid_values}. Value given = {value_given}")


@Field.parameter
class ValidValues(FieldParameter):
    __key__ = 'valid_values'
    __label__ = 'specific_value'
    __rules__ = Rules([BasicParameterValueTypeValidationRule((list, tuple, set))])
    __prior_handler__ = ArbitraryAnnotation
    __pass_on_errors__ = [MissingFieldValuesException]

    def _handle_values(self, model_instance, values, stage):
        val = values[self._field_key]

        if val not in self.param_val:
            getattr(model_instance, NamespacesConsts.EXCEPTIONS).append(NotAValidValue(self.param_val, val))

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_valid_values_field_parameter(self, context)
