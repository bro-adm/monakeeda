from monakeeda.base import FieldParameter, Rules, Field, Stages
# from monakeeda.base.fields.default_parameter import DefaultParameter
from ..rules import CallableParameterSignatureValidationRule
from .default_field_parameter import DefaultParameter


@Field.parameter
class DefaultFactory(FieldParameter):
    __key__ = 'default_factory'
    __label__ = 'default_provider'
    __prior_handler__ = DefaultParameter
    __rules__ = Rules([CallableParameterSignatureValidationRule(0)])

    def handle_values(self, model_instance, values, stage) -> dict:
        if stage == Stages.INIT:
            return {self._field_key: self.param_val()}

        return {}
