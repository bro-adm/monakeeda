from monakeeda.base import FieldParameter, Rules, Field, Stages
from .exceptions import ConstError
from ..rules import BasicParameterValueTypeValidationRule


@Field.parameter
class AllowMutation(FieldParameter):
    __key__ = 'const'
    __label__ = 'mutation'
    __rules__ = Rules([BasicParameterValueTypeValidationRule(bool)])

    def values_handler(self, model_instance, values, stage):
        if stage == Stages.UPDATE:
            curr_val = getattr(model_instance, self._field_key)
            new_val = values[self._field_key]

            if self.param_val and new_val != curr_val:
                raise ConstError(curr_val, new_val)

        return values
