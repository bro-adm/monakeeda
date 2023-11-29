import inspect
from typing import Any

from monakeeda.base import FieldParameter, Field, ExceptionsDict, BaseMonkey
from .consts import KnownLabels
from .explode_field_parameter import ExplodeFieldParameter
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..known_builders import ParameterValueTypeValidator


class AliasInfo(BaseMonkey, delay=True):
    key: str
    override_set_input: bool = False

    class Config:
        validate_missing_fields = True


@Field.parameter
class AliasFieldParameter(FieldParameter):
    __key__ = 'alias'
    __prior_handler__ = ExplodeFieldParameter
    __builders__ = [ParameterValueTypeValidator((str, AliasInfo))]

    @classmethod
    @property
    def label(cls) -> str:
        return KnownLabels.ALIAS_PROVIDER

    def is_collision(self, other) -> bool:
        super().is_collision(other)
        return False

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        super()._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)

        if isinstance(self.param_val, str):
            self.param_val = AliasInfo(key=self.param_val)

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        set_input = values.get(self.scope, inspect._empty)

        if set_input == inspect._empty or self.param_val.override_set_input:
            values.setdefault(self.param_val.key, inspect._empty)
            field_val_by_alias = values.pop(self.param_val.key)  # in order to remove the extra created field

            # alias takes priority over the actual field key
            if field_val_by_alias != inspect._empty:
                values[self.scope] = field_val_by_alias

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_alias_field_parameter(self, context)
