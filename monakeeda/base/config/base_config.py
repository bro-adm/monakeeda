from abc import ABC
from typing import Any, Union

from monakeeda.consts import NamespacesConsts
from ..component import ConfigurableComponent, Parameter
from ..fields import NoField
from ..operator import OperatorVisitor


class ConfigParameter(Parameter, ABC):
    """
    Just a class for simple differentiating between parameters implementations
    """

    def build(self, monkey_cls, bases, monkey_attrs):
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.CONFIG][self.__key__] = self.param_val


class Config(ConfigurableComponent[ConfigParameter]):
    """
    Just a class for simple differentiating between configurable component implementations
    """

    __label__ = 'config'
    __prior_handler__ = NoField

    def build(self, monkey_cls, bases, monkey_attrs):
        pass

    def _handle_values(self, model_instance, values, stage):
        pass

    def accept_operator(self, operator_visitor: OperatorVisitor, context: Any):
        operator_visitor.operate_config(self, context)
