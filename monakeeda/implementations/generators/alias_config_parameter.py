from typing import Any

from monakeeda.base import ConfigParameter, Config, ExceptionsDict
from monakeeda.consts import NamespacesConsts, FieldConsts
from ..known_scopes import KnownScopes
from ..abstract import ABSTRACT_MANAGER
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..known_builders import ParameterCallableValueValidator, FieldsParameterTypesExtractor


@Config.parameter
class AliasGenerator(ConfigParameter):
    __key__ = 'alias_generator'
    __prior_handler__ = ABSTRACT_MANAGER
    __builders__ = [ParameterCallableValueValidator(1), FieldsParameterTypesExtractor('alias')]

    @classmethod
    @property
    def label(cls) -> str:
        return 'aliases_generation'

    @property
    def scope(self) -> str:
        return KnownScopes.ParametersGenerators

    def is_collision(self, other) -> bool:
        super().is_collision(other)
        return False

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        pass

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        super()._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)

        alias_parameters_mapping = self._all_parameters_mapping['alias']

        for field_key, field_info in monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS].items():
            field = field_info[FieldConsts.FIELD]

            alias_val = self.param_val(field_key)
            alias_parameter_type = alias_parameters_mapping[field_key]
            alias_parameter = alias_parameter_type(alias_val, field_key)

            append = True
            for field_parameter in field._parameters:
                if alias_parameter == field_parameter:
                    append = False

            if append:
                monkey_cls.__type_organized_components__[alias_parameter_type.label].append(alias_parameter)  # adds to the currently running for loop and for later value handlers run order
                field._parameters.append(alias_parameter)  # added for consistency

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_alias_generator_config_parameter(self, context)
