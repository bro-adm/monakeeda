from monakeeda.base import ConfigParameter, Config, Rules
from monakeeda.consts import NamespacesConsts, FieldConsts
from .field_parameter import Alias
from ..rules import CallableParameterSignatureValidationRule, AllModelFieldsAcknowledgeParameterRule


@Config.parameter
class AliasGenerator(ConfigParameter):
    __key__ = 'alias_generator'
    __label__ = 'alias_generator'
    __rules__ = Rules([CallableParameterSignatureValidationRule(1), AllModelFieldsAcknowledgeParameterRule('alias')])

    def values_handler(self, model_instance, values, stage):
        return values

    def _find_alias_field_parameter_cls(self, field_cls):
        # rules validate the unwanted scenario where the filed cls does not acknowledge alias setup

        return \
            list(
                filter(
                    lambda field_parameter: field_parameter.__key__ == Alias.__key__,
                    field_cls.__parameters_components__
                )
            )[0]

    def _set_cls_landscape(self, monkey_cls, bases, monkey_attrs):
        for field_key, field_info in monkey_cls.__map__[NamespacesConsts.FIELDS].items():
            field = field_info[FieldConsts.FIELD]

            if Alias.__key__ not in field_info:
                alias_val = self.param_val(field_key)
                alias_parameter_type = self._find_alias_field_parameter_cls(field)
                alias_parameter = alias_parameter_type(alias_val)  # currently I only know to initialize the parameter in a single way
                alias_parameter._field_key = field_key

                field._initialized_params.append(alias_parameter)
                alias_parameter._set_cls_landscape(monkey_cls, bases, monkey_attrs)
