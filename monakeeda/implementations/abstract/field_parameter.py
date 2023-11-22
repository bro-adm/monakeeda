from typing import Any

from monakeeda.base import FieldParameter, Field, ExceptionsDict
from monakeeda.consts import NamespacesConsts
from .annotation import Abstract
from .exceptions import AbstractFieldFoundError
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..known_builders import ParameterValueTypeValidator


@Field.parameter
class AbstractParameter(FieldParameter):
    __key__ = 'abstract'
    __label__ = 'abstract'
    __builders__ = [ParameterValueTypeValidator(bool)]
    __prior_handler__ = Abstract

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        if self.param_val:
            exceptions[self.scope].append(AbstractFieldFoundError(self._field_key))

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_abstract_field_parameter(self, context)
