import inspect
import os
from typing import Any

from monakeeda.base import Field, Stages, ExceptionsDict, FieldParameter, BaseMonkey
from monakeeda.consts import NamespacesConsts, FieldConsts
from .alias_field_parameter import AliasFieldParameter
from .consts import KnownLabels
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..known_builders import ParameterValueTypeValidator


class EnvInfo(BaseMonkey, delay=True):
    key: str
    should_exist_on_build: bool = True
    use_always: bool = False
    fail_on_missing: bool = False
    override_set_input: bool = False

    class Config:
        validate_missing_fields = True


@Field.parameter
class EnvFieldParameter(FieldParameter):
    __key__ = 'env'
    __prior_handler__ = AliasFieldParameter
    __builders__ = [ParameterValueTypeValidator((str, EnvInfo))]

    @classmethod
    @property
    def label(cls) -> str:
        return KnownLabels.EXTERNAL_PROVIDER

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        super()._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)

        if isinstance(self.param_val, str):
            self.param_val = EnvInfo(key=self.param_val)

        if self.param_val.fail_on_missing:
            monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.REQUIRED] = False

        if self.param_val.should_exist_on_build:
            value = os.environ.get(self.param_val.key, inspect._empty)
            if value == inspect._empty:
                exceptions[self.scope].append(ValueError(f"{self.representor} missing -> {self.param_val.key}"))
                
    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        set_input = values.get(self.scope, inspect._empty)

        if set_input != inspect._empty or self.param_val.override_set_input or self.param_val.use_always or stage == Stages.INIT:
            value = os.environ.get(self.param_val.key, inspect._empty)
            if value != inspect._empty:
                values[self.scope] = value
            elif self.param_val.fail_on_missing:
                exceptions[self.scope].append(ValueError(f"{self.representor} missing -> {self.param_val.key}"))

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        pass
