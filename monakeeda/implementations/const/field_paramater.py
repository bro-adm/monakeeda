from typing import Any, Union

from monakeeda.base import FieldParameter, Rules, Field, Stages
from .exceptions import ConstError
from ..rules import BasicParameterValueTypeValidationRule
from .annotation import Const
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor


@Field.parameter
class AllowMutation(FieldParameter):
    __key__ = 'const'
    __label__ = 'mutation'
    __rules__ = Rules([BasicParameterValueTypeValidationRule(bool)])
    __prior_handler__ = Const

    def handle_values(self, model_instance, values, stage) -> Union[Exception, None]:
        if stage == Stages.UPDATE:
            curr_val = getattr(model_instance, self._field_key)
            new_val = values[self._field_key]

            if self.param_val and new_val != curr_val:
                return ConstError(curr_val, new_val)

        return

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_const_field_parameter(self, context)