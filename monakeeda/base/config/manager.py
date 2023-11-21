from typing import List

from monakeeda.consts import NamespacesConsts, ConfigConsts
from monakeeda.helpers import get_cls_attrs
from .base_config import ConfigParameter
from ..component import Component
from ..meta import ConfigurableComponentManager


class ConfigManager(ConfigurableComponentManager[ConfigParameter]):
    """
    The Configs concept allows for multiple Config classes (one is natively implemented).
    The Config classes types are overrideable via the class name.

    The Config Manager responsibility, just like most other Component Manager is to find the relevant components, build them
    and manage inheritance collisions.

    By default, all model inheritances will automatically build the current Config classes by:
        - merging the bases parameters with collision management
        - overriding merges via current cls parameters
    """

    def __init__(self, configs_map):
        self._configs_map = configs_map

    def _components(self, monkey_cls) -> List[Component]:
        configs = monkey_cls.struct[NamespacesConsts.CONFIGS]

        components = []
        for config_info in configs.values():
            if config_info:
                config = config_info[ConfigConsts.OBJECT]

                components.append(config)
                components.extend(config._parameters)

        return components

    def _set_by_base(self, monkey_cls, base, attrs, collisions):
        for config_name, config_type in self._configs_map.items():
            config_collisions = collisions.setdefault(config_name, [])

            current_config = monkey_cls.struct[NamespacesConsts.CONFIGS][config_name].setdefault(ConfigConsts.OBJECT, None)
            current_parameters = current_config._parameters if current_config else []

            base_config = base.struct[NamespacesConsts.CONFIGS][config_name].setdefault(ConfigConsts.OBJECT, None)
            base_parameters = base_config._parameters if base_config else []

            merged_parameters = self._manage_parameters_inheritance(base_parameters, current_parameters, config_collisions, is_bases=True)

            initialized_config = config_type.override_init(merged_parameters, unused_params={})
            monkey_cls.struct[NamespacesConsts.CONFIGS][config_name][ConfigConsts.OBJECT] = initialized_config

    def _set_curr_cls(self, monkey_cls, bases, monkey_attrs):
        for config_name, config_type in self._configs_map.items():
            config_cls = getattr(monkey_cls, config_name, None)

            if config_cls:
                bases_initialized_config = monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.CONFIGS][config_name].setdefault(ConfigConsts.OBJECT, None)
                bases_parameters = bases_initialized_config._parameters if bases_initialized_config else []

                config_attrs = get_cls_attrs(config_cls)
                new_parameters, unused_params = config_type.initiate_params(config_attrs, config_cls_name=config_name)

                merged_parameters = self._manage_parameters_inheritance(bases_parameters, new_parameters)
                initialized_config = config_type.override_init(merged_parameters, unused_params)

                monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.CONFIGS][config_name][ConfigConsts.OBJECT] = initialized_config

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: List[Exception], main_builder):
        monkey_attrs[NamespacesConsts.STRUCT].setdefault(NamespacesConsts.CONFIGS, {})

        for config_name, config_type in self._configs_map.items():
            monkey_cls.struct[NamespacesConsts.CONFIGS].setdefault(config_name, {})

        super()._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)
