import inspect

from monakeeda.base import FieldParameter, Rules, Field
from ..rules import BasicParameterValueTypeValidationRule


@Field.parameter
class Alias(FieldParameter):
    __key__ = 'alias'
    __label__ = 'alias'
    __rules__ = Rules([BasicParameterValueTypeValidationRule(str)])

    def _values_handler(self, priority, model_instance, values, stage) -> dict:
        updated_values = {}

        values.setdefault(self.param_val, inspect._empty)
        field_val_by_alias = values.pop(self.param_val)

        if field_val_by_alias != inspect._empty:
            updated_values[self._field_key] = field_val_by_alias

        return updated_values
