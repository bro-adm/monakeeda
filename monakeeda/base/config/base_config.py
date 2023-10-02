from abc import ABC

from ..component import ConfigurableComponent, Parameter
from ..fields import Field


class ConfigParameter(Parameter, ABC):
    """
    Just a class for simple differentiating between parameters implementations
    """

    pass


class Config(ConfigurableComponent[ConfigParameter]):
    """
    Just a class for simple differentiating between configurable component implementations
    """

    __label__ = 'config'
    __prior_handler__ = Field

    def build(self, monkey_cls, bases, monkey_attrs):
        pass

    def handle_values(self, model_instance, values, stage) -> dict:
        return {}
