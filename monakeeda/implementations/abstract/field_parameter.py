from monakeeda.base import FieldParameter, Rules, Field
from .exceptions import AbstractFieldFoundError
from ..rules import BasicParameterValueTypeValidationRule


@Field.parameter
class AbstractParameter(FieldParameter):
    __key__ = 'abstract'
    __label__ = 'abstract'
    __rules__ = Rules([BasicParameterValueTypeValidationRule(bool)])

    def _values_handler(self, priority, model_instance, values, stage) -> dict:
        if self.param_val:
            raise AbstractFieldFoundError(self._field_key)

        return values
