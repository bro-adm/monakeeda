from monakeeda.base import FieldParameter, Rules, Field, Stages
from ..rules import CallableParameterSignatureValidationRule


@Field.parameter
class DefaultFactory(FieldParameter):
    __key__ = 'default_factory'
    __label__ = 'default_provider'
    __rules__ = Rules([CallableParameterSignatureValidationRule(0)])

    def _values_handler(self, priority, model_instance, values, stage):
        if stage == Stages.INIT:
            return {self._field_key: self.param_val()}

        return {}
