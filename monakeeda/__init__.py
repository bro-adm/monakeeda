from .base import Field, Config, labeled_components
from .implementations import *
from .monkey_model import MonkeyModel, generate_model


def log_main_information():
    from .base import labeled_components, all_configs, all_operators
    from .logger import logger, STAGE, MONKEY

    for label, components in labeled_components.items():
        for component in components:
            logger.info(f"\t{label} -> {component}", extra={STAGE: "All Components", MONKEY: "MONAKEEDA"})

    for config_name, config_cls in all_configs.items():
        logger.info(f"\t{config_name} -> {config_cls}", extra={STAGE: "All Configs", MONKEY: "MONAKEEDA"})

    for operator_key, operator in all_operators.items():
        logger.info(f"\t{operator_key} -> {operator}", extra={STAGE: "All Operators", MONKEY: "MONAKEEDA"})
