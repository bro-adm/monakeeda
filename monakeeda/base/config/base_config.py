from abc import ABC
from typing import Any, Type

from monakeeda.consts import NamespacesConsts, ConfigConsts
from ..component import ConfigurableComponent, Parameter
from ..fields import NoField
from ..operator import OperatorVisitor


class ConfigParameter(Parameter, ABC):
    """
    Just a class for simple differentiating between parameters implementations
    """

    def __init__(self, config_cls_name: str, param_val):
        self._config_cls_name = config_cls_name
        super().__init__(param_val)

    def build(self, monkey_cls, bases, monkey_attrs):
        pass
        # monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.CONFIGS][self._config_cls_name][ConfigConsts.COMPONENTS].append(self)
        # monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.CONFIGS][self._config_cls_name][self.__key__] = self.param_val


all_configs = {}


class Config(ConfigurableComponent[ConfigParameter]):
    """
    Just a class for simple differentiating between configurable component implementations
    """

    __label__ = 'config'
    __prior_handler__ = NoField

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        all_configs[cls.__name__] = cls

    def build(self, monkey_cls, bases, monkey_attrs):
        pass
        # monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.CONFIGS][self.__class__.__name__][ConfigConsts.COMPONENTS] = self._parameters

    def _handle_values(self, model_instance, values, stage):
        pass

    @classmethod
    def _initiate_param(cls, param_cls: Type[ConfigParameter], param_val) -> ConfigParameter:
        return param_cls(cls.__name__, param_val)

    def accept_operator(self, operator_visitor: OperatorVisitor, context: Any):
        operator_visitor.operate_config(self, context)


all_configs[Config.__name__] = Config
