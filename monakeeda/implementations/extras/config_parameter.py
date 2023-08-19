from enum import Enum

from monakeeda.base import ConfigParameter, Config, Rules
from monakeeda.consts import NamespacesConsts
from ..rules import BasicParameterValueTypeValidationRule


class Extras(Enum):
    ALLOW = 'allow'
    IGNORE = 'ignore'


@Config.parameter
class ExtrasParameter(ConfigParameter):
    __key__ = 'extra'
    __label__ = 'extras'
    __rules__ = Rules([BasicParameterValueTypeValidationRule(Extras)])
    __priority__ = 4

    def _values_handler(self, priority, model_instance, values, stage) -> dict:
        if self.param_val == Extras.IGNORE:
            acknowledged_fields = model_instance.__map__[NamespacesConsts.FIELDS_KEYS]
            unacknowledged = []

            for key in values:
                if key not in acknowledged_fields:
                    unacknowledged.append(key)

            for key in unacknowledged:
                values.pop(key)

        return {}

    def _set_cls_landscape(self, monkey_cls, bases, monkey_attrs):
        pass
