from enum import Enum
from typing import Any

from monakeeda.base import ConfigParameter, Config, ExceptionsDict
from monakeeda.consts import NamespacesConsts
from ..const import AllowMutation
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..known_builders import ParameterValueTypeValidator


class Extras(Enum):
    ALLOW = 'allow'
    IGNORE = 'ignore'
    KEEP_USED = 'keep_used'


@Config.parameter
class ExtrasParameter(ConfigParameter):
    __key__ = 'extra'
    __label__ = 'extras'
    __builders__ = [ParameterValueTypeValidator(Extras)]
    __prior_handler__ = AllowMutation

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        if self.param_val != Extras.ALLOW:
            fields = list(getattr(model_instance, NamespacesConsts.STRUCT)[NamespacesConsts.FIELDS].keys())

            if self.param_val == Extras.IGNORE:
                fields = list(model_instance.struct[NamespacesConsts.ANNOTATIONS].keys())
                # struct annotations is the compartment which lists all the fields directly set without any dependency setup...

            unacknowledged = []

            for key in values:
                if key not in fields:
                    unacknowledged.append(key)

            for key in unacknowledged:
                values.pop(key)

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        pass

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_extras_config_parameter(self, context)
