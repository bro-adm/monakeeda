from abc import ABC

from ..component import ConfigurableComponent, Parameter


class ConfigParameter(Parameter, ABC):
    """
    Just a class for simple differentiating between parameters implementations
    """

    pass


# TODO: add annotation_mapping parameter for config
class Config(ConfigurableComponent[ConfigParameter]):
    """
    Just a class for simple differentiating between configurable component implementations
    """

    pass
