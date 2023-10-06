import inspect
from typing import Any, Union

from .base_field_parameter import BaseInputFieldParameter
from monakeeda.base import Rules, Stages
from monakeeda.consts import FieldConsts, NamespacesConsts
from ..rules import BasicParameterValueTypeValidationRule
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..alias import Alias
from ... import Field


@Field.parameter
class NoInputFieldParameter(BaseInputFieldParameter):
    __key__ = 'no_input'
    __prior_handler__ = Alias
    __rules__ = Rules([BasicParameterValueTypeValidationRule(bool)])

    def handle_values(self, model_instance, values, stage) -> Union[Exception, None]:
        if stage == Stages.INIT and self.param_val:
            values.setdefault(self._field_key, inspect._empty)
            values.pop(self._field_key)  # in order to remove the extra created field

        return

    def build(self, monkey_cls, bases, monkey_attrs):
        super().build(monkey_cls, bases, monkey_attrs)
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.REQUIRED] = False

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_no_input_field_parameter(self, context)