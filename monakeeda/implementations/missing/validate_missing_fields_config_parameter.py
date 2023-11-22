from typing import Any

from monakeeda.base import ConfigParameter, Config
from monakeeda.consts import NamespacesConsts, FieldConsts
from monakeeda.helpers import ExceptionsDict
from .errors import MissingFieldValuesException
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..optional import OptionalAnnotation
from ..known_builders import ParameterAllowedValuesValidatorBuilder


@Config.parameter
class ValidateMissingFieldsConfigParameter(ConfigParameter):
    __key__ = 'validate_missing_fields'
    __label__ = 'missing_values_manager'
    __builders__ = [ParameterAllowedValuesValidatorBuilder([True])]
    __prior_handler__ = OptionalAnnotation

    def _handle_values(self, model_instance, values, stage):
        if self.param_val:
            fields_info = getattr(model_instance, NamespacesConsts.STRUCT)[NamespacesConsts.FIELDS]

            missing_fields = []

            for key, field_info in fields_info.items():
                if field_info[FieldConsts.REQUIRED] and key not in values:
                    missing_fields.append(key)

            if missing_fields:
                getattr(model_instance, NamespacesConsts.EXCEPTIONS).append(MissingFieldValuesException(missing_fields))

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        pass

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_validate_missing_fields_config_parameter(self, context)
