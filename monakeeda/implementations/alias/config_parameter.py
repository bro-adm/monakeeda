from monakeeda.base import ConfigParameter, Config, Rules, FieldParameter
from monakeeda.consts import NamespacesConsts, FieldConsts
from ..default import DefaultFactory
# from .field_parameter import Alias
from ..rules import CallableParameterSignatureValidationRule, AllModelFieldsAcknowledgeParameterRule


@Config.parameter
class AliasGenerator(ConfigParameter):
    __key__ = 'alias_generator'
    __label__ = 'alias_generator'
    __prior_handler__ = DefaultFactory
    __rules__ = Rules([CallableParameterSignatureValidationRule(1), AllModelFieldsAcknowledgeParameterRule('alias')])

    def handle_values(self, model_instance, values, stage) -> dict:
        return values

    def _get_field_alias_component(self, field_cls) -> FieldParameter:
        # rules validate the unwanted scenario where the filed cls does not acknowledge alias setup

        return \
            list(
                filter(
                    lambda field_parameter: field_parameter.__key__ == 'alias',
                    field_cls.__parameter_components__
                )
            )[0]

    def build(self, monkey_cls, bases, monkey_attrs):
        for field_key, field_info in monkey_cls.__map__[NamespacesConsts.FIELDS].items():
            field = field_info[FieldConsts.FIELD]

            if 'alias' not in field_info:
                alias_val = self.param_val(field_key)
                alias_parameter_type = self._get_field_alias_component(field)
                alias_parameter = alias_parameter_type(alias_val)  # currently I only know to initialize the parameter in a single way
                alias_parameter._field_key = field_key

                field._initialized_params.append(alias_parameter)

