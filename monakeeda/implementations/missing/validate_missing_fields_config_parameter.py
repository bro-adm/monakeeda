from typing import Any

from monakeeda.base import ConfigParameter, Config, ExceptionsDict
from monakeeda.consts import NamespacesConsts, FieldConsts
from .exceptions import MissingFieldValueException
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..known_builders import ParameterAllowedValuesValidator
from ..known_scopes import KnownScopes
from ..optional import OptionalAnnotation


@Config.parameter
class ValidateMissingFieldsConfigParameter(ConfigParameter):
    __key__ = 'validate_missing_fields'
    __builders__ = [ParameterAllowedValuesValidator([True])]
    __prior_handler__ = OptionalAnnotation

    @classmethod
    @property
    def label(cls) -> str:
        return "missing_values_manager"

    @property
    def scope(self) -> str:
        return KnownScopes.ValuesManagers

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        if self.param_val:
            fields_info = getattr(model_instance, NamespacesConsts.STRUCT)[NamespacesConsts.FIELDS]
            exception = MissingFieldValueException()

            for key, field_info in fields_info.items():
                if field_info[FieldConsts.REQUIRED] and key not in values:
                    exceptions[key].append(exception)

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        pass

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_validate_missing_fields_config_parameter(self, context)
