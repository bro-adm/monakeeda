from typing import Any

from monakeeda.base import Field, Stages
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..input import NoInputFieldParameter
from .base import BaseDefaultFieldParameter


@Field.parameter
class DefaultFieldParameter(BaseDefaultFieldParameter):
    __key__: str = 'default'
    __prior_handler__ = NoInputFieldParameter

    def handle_values(self, model_instance, values, stage) -> dict:
        if stage == Stages.INIT:
            return {self._field_key: values.get(self._field_key, self.param_val)}

        return {}

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_default_field_parameter(self, context)
