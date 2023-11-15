from abc import ABC
from typing import Any, List, Dict

from monakeeda.consts import FieldConsts, NamespacesConsts
from ..component import Parameter, ConfigurableComponent
from ..operator import OperatorVisitor


class FieldParameter(Parameter, ABC):

    def __init__(self, param_val, field_key):
        self._field_key = field_key
        super().__init__(param_val)

    def __eq__(self, other):
        if not isinstance(other, FieldParameter):
            return NotImplemented
        return self._field_key == other._field_key and self.param_val == other.param_val

    def build(self, monkey_cls, bases, monkey_attrs):
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.COMPONENTS].append(self)


class Field(ConfigurableComponent[FieldParameter]):
    __label__ = 'field'

    @classmethod
    def override_init(cls, field_key: str, parameters: List[FieldParameter], unused_params: Dict[str, Any]):
        instance = super().override_init(parameters, unused_params)
        instance._field_key = field_key

        return instance

    def build(self, monkey_cls, bases, monkey_attrs):
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.REQUIRED] = True
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.COMPONENTS].append(self)

    def _handle_values(self, model_instance, values, stage):
        pass

    def accept_operator(self, operator_visitor: OperatorVisitor, context: Any):
        operator_visitor.operate_field(self, context)


class NoField(Field, copy_parameter_components=False):
    """
    copy_parameter_components=False -> will keep the same list memory context as the Field Component itself ->
    meaning all the parameters available to it will be available here which is important for cases parameter
    initializations are added by code and not user like alias in AliasGenerator.
    """
    __prior_handler__ = Field

    def __init__(self):
        # hard set: no params available for initialization
        super(NoField, self).__init__()
