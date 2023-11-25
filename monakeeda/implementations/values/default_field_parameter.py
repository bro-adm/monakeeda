from typing import Any

from monakeeda.base import Field, Stages, ExceptionsDict
from .base import BaseValueFieldParameter
from .value_field_parameter import ValueFieldParameter
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor


@Field.parameter
class DefaultFieldParameter(BaseValueFieldParameter):
    __key__ = 'default'
    __prior_handler__ = ValueFieldParameter

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        if stage == Stages.INIT:
            value = values.get(self._field_key, self.param_val)
            values[self._field_key] = value

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_default_field_parameter(self, context)
