from typing import Any

from monakeeda.base import ConfigParameter, Config, Rules, get_parameter_component_by_key
from monakeeda.consts import NamespacesConsts, FieldConsts
from ..abstract import AbstractParameter
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..rules import CallableParameterSignatureValidationRule, AllModelFieldsAcknowledgeParameterRule


@Config.parameter
class AliasGenerator(ConfigParameter):
    __key__ = 'alias_generator'
    __label__ = 'alias_generator'
    __prior_handler__ = AbstractParameter
    __rules__ = Rules([CallableParameterSignatureValidationRule(1), AllModelFieldsAcknowledgeParameterRule('alias')])

    def _handle_values(self, model_instance, values, stage):
        pass

    def build(self, monkey_cls, bases, monkey_attrs):
        super().build(monkey_cls, bases, monkey_attrs)

        for field_key, field_info in monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS].items():
            field = field_info[FieldConsts.FIELD]
            alias_parameter_type = get_parameter_component_by_key(field, 'alias')

            alias_val = self.param_val(field_key)
            alias_parameter = alias_parameter_type(alias_val, field_key)

            append = True
            for field_parameter in field._parameters:
                if alias_parameter == field_parameter:
                    append = False

            if append:
                monkey_cls.__organized_components__[alias_parameter_type].insert(0, alias_parameter)  # adds to the currently running for loop and for later value handlers run order
                field._parameters.append(alias_parameter)  # only to be nice for future use cases
                monkey_attrs[NamespacesConsts.COMPONENTS].append(alias_parameter)  # added it only to be nice - not required - post usage of this list

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_alias_generator_config_parameter(self, context)
