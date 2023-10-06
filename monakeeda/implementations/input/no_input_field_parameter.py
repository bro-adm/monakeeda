import inspect
from typing import Any

from .base_field_parameter import BaseInputFieldParameter
from monakeeda.base import Rules, Stages
from ..rules import BasicParameterValueTypeValidationRule
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..alias import Alias
from ... import Field


@Field.parameter
class NoInputFieldParameter(BaseInputFieldParameter):
    __key__ = 'no_input'
    __prior_handler__ = Alias
    __rules__ = Rules([BasicParameterValueTypeValidationRule(bool)])

    def handle_values(self, model_instance, values, stage) -> dict:
        if stage == Stages.INIT and self.param_val:
            values.setdefault(self._field_key, inspect._empty)
            values.pop(self._field_key)  # in order to remove the extra created field

        return {}

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_no_input_field_parameter(self, context)