from abc import ABC
from typing import Any

from ..component import ConfigurableComponent, Parameter
from ..fields import NoField
from ..operator import OperatorVisitor


class ConfigParameter(Parameter, ABC):
    """
    Just a class for simple differentiating between parameters implementations
    """

    def __init__(self, param_val, config_cls_name: str):
        super().__init__(param_val)
        self._config_cls_name = config_cls_name

    def build(self, monkey_cls, bases, monkey_attrs):
        pass


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

    def _handle_values(self, model_instance, values, stage):
        pass

    def accept_operator(self, operator_visitor: OperatorVisitor, context: Any):
        operator_visitor.operate_config(self, context)


all_configs[Config.__name__] = Config
