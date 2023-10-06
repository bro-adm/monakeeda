from typing import Any, Union

from monakeeda.base import FieldParameter, Rules, Field
from .exceptions import AbstractFieldFoundError
from .annotation import Abstract
from ..rules import BasicParameterValueTypeValidationRule
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor


@Field.parameter
class AbstractParameter(FieldParameter):
    __key__ = 'abstract'
    __label__ = 'abstract'
    __rules__ = Rules([BasicParameterValueTypeValidationRule(bool)])
    __prior_handler__ = Abstract

    def handle_values(self, model_instance, values, stage) -> Union[Exception, None]:
        if self.param_val:
            return AbstractFieldFoundError(self._field_key)

        return

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_abstract_field_parameter(self, context)
