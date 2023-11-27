import inspect
from typing import Any

from monakeeda.base import FieldParameter, Field, ExceptionsDict
from ..generators import AliasGenerator
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..known_builders import ParameterValueTypeValidator


@Field.parameter
class Alias(FieldParameter):
    __key__ = 'alias'
    __prior_handler__ = AliasGenerator
    __builders__ = [ParameterValueTypeValidator(str)]

    @classmethod
    @property
    def label(cls) -> str:
        return 'alias'

    def is_collision(self, other) -> bool:
        super().is_collision(other)
        return False

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        values.setdefault(self.param_val, inspect._empty)
        field_val_by_alias = values.pop(self.param_val)  # in order to remove the extra created field

        # alias takes priority over the actual field key
        if field_val_by_alias != inspect._empty:
            values[self.scope] = field_val_by_alias

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_alias_field_parameter(self, context)
