from typing import Any, Union

from monakeeda.base import FieldParameter, Rules, Field
from ..rules import BasicParameterValueTypeValidationRule
from ..basic_annotations import DictAnnotation
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from monakeeda.consts import NamespacesConsts
from ..missing.errors import MissingFieldValuesException


class NotAValidValue(ValueError):
    def __init__(self, valid_values, value_given):
        super(NotAValidValue, self).__init__(
            f"Valid values = {valid_values}. Value given = {value_given}")


@Field.parameter
class ValidValues(FieldParameter):
    __key__ = 'valid_values'
    __label__ = 'specific_value'
    __rules__ = Rules([BasicParameterValueTypeValidationRule((list, tuple, set))])
    __prior_handler__ = DictAnnotation
    __pass_on_errors__ = [MissingFieldValuesException]

    def _handle_values(self, model_instance, values, stage):
        val = values[self._field_key]

        if val not in self.param_val:
            getattr(model_instance, NamespacesConsts.EXCEPTIONS).append(NotAValidValue(self.param_val, val))

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_valid_values_field_parameter(self, context)
