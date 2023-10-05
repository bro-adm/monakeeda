from typing import Any

from monakeeda.base import ConfigParameter, Config, Rules, get_parameter_component_by_label
from monakeeda.consts import NamespacesConsts, FieldConsts
from ..default import DefaultFactoryFieldParameter
from ..rules import CallableParameterSignatureValidationRule, AllModelFieldsAcknowledgeParameterRule
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor


@Config.parameter
class AliasGenerator(ConfigParameter):
    __key__ = 'alias_generator'
    __label__ = 'alias_generator'
    __prior_handler__ = DefaultFactoryFieldParameter
    __rules__ = Rules([CallableParameterSignatureValidationRule(1), AllModelFieldsAcknowledgeParameterRule('alias')])

    def handle_values(self, model_instance, values, stage) -> dict:
        return values

    def build(self, monkey_cls, bases, monkey_attrs):
        for field_key, field_info in monkey_cls.__map__[NamespacesConsts.FIELDS].items():
            field = field_info[FieldConsts.FIELD]
            alias_parameter_type = get_parameter_component_by_label(field, 'alias')

            alias_val = self.param_val(field_key)
            alias_parameter = alias_parameter_type(alias_val)
            alias_parameter._field_key = field_key

            field._initialized_params.append(alias_parameter)
            monkey_cls.__organized_components__[str(alias_parameter_type)].append(alias_parameter)

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_alias_generator_config_parameter(self, context)
