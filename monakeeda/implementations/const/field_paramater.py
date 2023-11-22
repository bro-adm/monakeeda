from typing import Any

from monakeeda.base import FieldParameter, Field, Stages
from monakeeda.consts import NamespacesConsts
from .annotation import Const
from .exceptions import ConstError
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..known_builders import ParameterValueTypeValidator


@Field.parameter
class AllowMutation(FieldParameter):
    __key__ = 'const'
    __label__ = 'mutation'
    __builders__ = [ParameterValueTypeValidator(bool)]
    __prior_handler__ = Const

    def _handle_values(self, model_instance, values, stage):
        if stage == Stages.UPDATE:
            curr_val = getattr(model_instance, self._field_key)
            new_val = values[self._field_key]

            if self.param_val and new_val != curr_val:
                getattr(model_instance, NamespacesConsts.EXCEPTIONS).append(ConstError(curr_val, new_val))

        return

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_const_field_parameter(self, context)