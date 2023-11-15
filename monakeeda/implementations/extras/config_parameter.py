from enum import Enum
from typing import Any

from monakeeda.base import ConfigParameter, Config, Rules
from monakeeda.consts import NamespacesConsts, FieldConsts
from ..const import AllowMutation
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..rules import BasicParameterValueTypeValidationRule


class Extras(Enum):
    ALLOW = 'allow'
    IGNORE = 'ignore'
    KEEP_USED = 'keep_used'


@Config.parameter
class ExtrasParameter(ConfigParameter):
    __key__ = 'extra'
    __label__ = 'extras'
    __rules__ = Rules([BasicParameterValueTypeValidationRule(Extras)])
    __prior_handler__ = AllowMutation

    def _handle_values(self, model_instance, values, stage):
        if self.param_val != Extras.ALLOW:
            fields = getattr(model_instance, NamespacesConsts.STRUCT)[NamespacesConsts.FIELDS]

            if self.param_val == Extras.IGNORE:
                # fields with no Field attr are not schema fields and in this if they are ignored
                fields = dict(filter(lambda tup: tup[1].get(FieldConsts.FIELD, False), fields.items()))

            unacknowledged = []

            for key in values:
                if key not in fields:
                    unacknowledged.append(key)

            for key in unacknowledged:
                values.pop(key)

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_extras_config_parameter(self, context)
