import inspect
from typing import Any

from monakeeda.base import FieldParameter, Rules, Field
from .config_parameter import AliasGenerator
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..rules import BasicParameterValueTypeValidationRule


@Field.parameter
class Alias(FieldParameter):
    __key__ = 'alias'
    __label__ = 'alias'
    __prior_handler__ = AliasGenerator
    __rules__ = Rules([BasicParameterValueTypeValidationRule(str)])

    def _handle_values(self, model_instance, values, stage):
        values.setdefault(self.param_val, inspect._empty)
        field_val_by_alias = values.pop(self.param_val)  # in order to remove the extra created field

        # alias takes priority over the actual field key
        if field_val_by_alias != inspect._empty:
            values[self._field_key] = field_val_by_alias

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_alias_field_parameter(self, context)
