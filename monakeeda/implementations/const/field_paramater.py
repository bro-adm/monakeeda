from typing import Any

from monakeeda.base import FieldParameter, Field, Stages, ExceptionsDict
from .annotation import Const
from .consts import MUTATION_MANAGER
from .exceptions import ConstError
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..known_builders import ParameterValueTypeValidator


@Field.parameter
class AllowMutation(FieldParameter):
    __key__ = 'const'
    __builders__ = [ParameterValueTypeValidator(bool)]
    __prior_handler__ = Const

    @classmethod
    @property
    def label(cls) -> str:
        return MUTATION_MANAGER

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        if stage == Stages.UPDATE:
            curr_val = getattr(model_instance, self._field_key)
            new_val = values[self._field_key]

            if self.param_val and new_val != curr_val:
                exceptions[self.scope].append(ConstError(curr_val, new_val))

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_const_field_parameter(self, context)