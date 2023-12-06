from typing import Any

from monakeeda.base import Field, Stages, ExceptionsDict, FieldParameter
from monakeeda.consts import NamespacesConsts, FieldConsts
from .consts import KnownLabels
from .env_field_parameter import EnvFieldParameter
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..known_builders import ParameterCallableValueValidator


@Field.parameter
class DefaultFactoryFieldParameter(FieldParameter):
    __key__ = 'default_factory'
    __prior_handler__ = EnvFieldParameter.label
    __builders__ = [ParameterCallableValueValidator(0)]

    @classmethod
    @property
    def label(cls) -> str:
        return KnownLabels.DEFAULT_PROVIDER

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        super()._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.REQUIRED] = False

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        if stage == Stages.INIT:
            value = values.get(self._field_key, self.param_val())
            values[self._field_key] = value

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_default_factory_field_parameter(self, context)
