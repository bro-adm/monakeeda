from typing import Any

from monakeeda.base import Rules, Field, Stages
from ..rules import CallableParameterSignatureValidationRule
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from .base import BaseDefaultFieldParameter
from .default_field_parameter import DefaultFieldParameter


@Field.parameter
class DefaultFactoryFieldParameter(BaseDefaultFieldParameter):
    __key__ = 'default_factory'
    __prior_handler__ = DefaultFieldParameter
    __rules__ = Rules([CallableParameterSignatureValidationRule(0)])

    def handle_values(self, model_instance, values, stage) -> dict:
        if stage == Stages.INIT:
            return {self._field_key: self.param_val()}

        return {}

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_default_factory_field_parameter(self, context)
