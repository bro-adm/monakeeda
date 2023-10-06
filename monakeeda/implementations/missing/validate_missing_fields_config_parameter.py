from typing import Union, Any

from monakeeda.base import ConfigParameter, Config, Rules
from monakeeda.consts import NamespacesConsts, FieldConsts
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..rules import AllowedValuesRule
from ..default import DefaultFactoryFieldParameter
from .errors import MissingFieldValuesException


@Config.parameter
class ValidateMissingFieldsConfigParameter(ConfigParameter):
    __key__ = 'validate_missing_fields'
    __label__ = 'values_manager'
    __rules__ = Rules([AllowedValuesRule([True])])
    __prior_handler__ = DefaultFactoryFieldParameter

    def handle_values(self, model_instance, values, stage) -> Union[Exception, None]:
        if self.param_val:
            fields_info = getattr(model_instance, NamespacesConsts.STRUCT)[NamespacesConsts.FIELDS]

            missing_fields = []

            for key, field_info in fields_info.items():
                if field_info[FieldConsts.REQUIRED] and key not in values:
                    missing_fields.append(key)

            if missing_fields:
                return MissingFieldValuesException(missing_fields)

        return

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_validate_missing_fields_config_parameter(self, context)
