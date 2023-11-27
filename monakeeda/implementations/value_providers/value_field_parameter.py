from typing import Any

from monakeeda.base import Field, Stages, ExceptionsDict
from .base import BaseValueFieldParameter
from ..alias import Alias
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor


@Field.parameter
class ValueFieldParameter(BaseValueFieldParameter):
    __key__ = 'value'
    __prior_handler__ = Alias

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        if stage == Stages.INIT:
            values[self._field_key] = self.param_val

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_default_field_parameter(self, context)
