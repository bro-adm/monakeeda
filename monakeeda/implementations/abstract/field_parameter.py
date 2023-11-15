from typing import Any

from monakeeda.base import FieldParameter, Rules, Field
from monakeeda.consts import NamespacesConsts
from .annotation import Abstract
from .exceptions import AbstractFieldFoundError
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..rules import BasicParameterValueTypeValidationRule


@Field.parameter
class AbstractParameter(FieldParameter):
    __key__ = 'abstract'
    __label__ = 'abstract'
    __rules__ = Rules([BasicParameterValueTypeValidationRule(bool)])
    __prior_handler__ = Abstract

    def _handle_values(self, model_instance, values, stage):
        if self.param_val:
            getattr(model_instance, NamespacesConsts.EXCEPTIONS).append(AbstractFieldFoundError(self._field_key))

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_abstract_field_parameter(self, context)
