from abc import ABC
from typing import Any

from ..component import ConfigurableComponent, Parameter
from ..exceptions_manager import ExceptionsDict
from ..fields import NoField
from ..operator import OperatorVisitor


class ConfigParameter(Parameter, ABC):
    """
    Conceptually just like the base Parameter Component, this one just get passed the Config Class name it gets initialized by.
    """

    def __init__(self, param_val, config_cls_name: str, is_managed=False):
        super().__init__(param_val, is_managed)
        self._config_cls_name = config_cls_name


all_configs = {}


class Config(ConfigurableComponent[ConfigParameter]):
    """
    A sub class of the Configurable Component for allowing different managed Parameter Components list.

    Initialized via the Configs Manager, which itself acknowledges a set of Configs by default via the all_configs dictionary.
    Allows override of a Config class "type" by class name.
    """

    __prior_handler__ = NoField

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        all_configs[cls.__name__] = cls

    @property
    def scope(self) -> str:
        return self.__class__.__name__

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        pass

    def accept_operator(self, operator_visitor: OperatorVisitor, context: Any):
        operator_visitor.operate_config(self, context)


all_configs[Config.__name__] = Config
