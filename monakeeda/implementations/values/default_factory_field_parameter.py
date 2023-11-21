from typing import Any

from monakeeda.base import Field, Stages
from .base import BaseValueFieldParameter
from .default_field_parameter import DefaultFieldParameter
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..known_builders import CallableParameterSignatureValidatorBuilder


@Field.parameter
class DefaultFactoryFieldParameter(BaseValueFieldParameter):
    __key__ = 'default_factory'
    __prior_handler__ = DefaultFieldParameter
    __builders__ = [CallableParameterSignatureValidatorBuilder(0)]

    def _handle_values(self, model_instance, values, stage):
        if stage == Stages.INIT:
            value = values.get(self._field_key, self.param_val())
            values[self._field_key] = value

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_default_factory_field_parameter(self, context)
