from abc import ABC
from typing import Any, Union

from monakeeda.consts import FieldConsts, NamespacesConsts
from ..component import Parameter, ConfigurableComponent
from ..operator import OperatorVisitor


class FieldParameter(Parameter, ABC):

    def __init__(self, param_val):
        self._field_key = None
        super().__init__(param_val)

    def build(self, monkey_cls, bases, monkey_attrs):
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][self.__key__] = self.param_val
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.COMPONENTS].append(self)


class Field(ConfigurableComponent[FieldParameter]):
    __label__ = 'field'

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
