from typing import Any

from monakeeda.consts import NamespacesConsts, FieldConsts
from monakeeda.base import Field, FieldParameter, Stages
from ..abstract import Abstract
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor


@Field.parameter
class DefaultParameter(FieldParameter):
    __key__: str = 'default'
    __label__ = 'default_provider'
    __prior_handler__ = Abstract

    def handle_values(self, model_instance, values, stage) -> dict:
        if stage == Stages.INIT:
            return {self._field_key: values.get(self._field_key, self.param_val)}

        return {}

    def build(self, monkey_cls, bases, monkey_attrs):
        super(DefaultParameter, self).build(monkey_cls, bases, monkey_attrs)
        monkey_cls.__map__[NamespacesConsts.FIELDS][self._field_key][FieldConsts.REQUIRED] = False

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_default_field_parameter(self, context)
