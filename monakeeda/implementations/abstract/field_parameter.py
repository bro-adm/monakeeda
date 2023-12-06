from typing import Any

from monakeeda.base import FieldParameter, Field, ExceptionsDict, Config
from .consts import ABSTRACT_MANAGER
from .exceptions import AbstractFieldFoundError
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..known_builders import ParameterValueTypeValidator


@Field.parameter
class AbstractParameter(FieldParameter):
    __key__ = 'abstract'
    __builders__ = [ParameterValueTypeValidator(bool)]
    __prior_handler__ = Config.label

    @classmethod
    @property
    def label(cls) -> str:
        return ABSTRACT_MANAGER

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        if self.param_val:
            exceptions[self.scope].append(AbstractFieldFoundError())

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_abstract_field_parameter(self, context)
