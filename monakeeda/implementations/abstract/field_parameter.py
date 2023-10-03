from monakeeda.base import FieldParameter, Rules, Field
from .exceptions import AbstractFieldFoundError
from .annotation import Abstract
from ..rules import BasicParameterValueTypeValidationRule


@Field.parameter
class AbstractParameter(FieldParameter):
    __key__ = 'abstract'
    __label__ = 'abstract'
    __rules__ = Rules([BasicParameterValueTypeValidationRule(bool)])
    __prior_handler__ = Abstract

    def handle_values(self, model_instance, values, stage) -> dict:
        if self.param_val:
            raise AbstractFieldFoundError(self._field_key)

        return values
