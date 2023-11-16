from abc import ABCMeta

from monakeeda.consts import NamespacesConsts, ComponentConsts
from monakeeda.logger import logger, STAGE, MONKEY
from .helpers import handle_class_inputs
from ..interfaces import RulesException


class MonkeyMeta(ABCMeta):
    def __new__(mcs, name, bases, attrs, **_):
        attrs[NamespacesConsts.STRUCT] = {}
        attrs[NamespacesConsts.COMPONENTS] = []
        attrs[NamespacesConsts.EXCEPTIONS] = RulesException(name, [])
        attrs[NamespacesConsts.TMP] = {}

        logger.info(f"Bases = {bases}", extra={STAGE: "META SETUP", MONKEY: name})
        logger.info(f"Attrs = {attrs}", extra={STAGE: "META SETUP", MONKEY: name})

        cls = super(MonkeyMeta, mcs).__new__(mcs, name, bases, attrs)
        return cls

    def __init__(cls, name, bases, attrs, component_managers=None, component_organizer=None, annotation_mapping=None, operators_visitors=None):
        handle_class_inputs(cls, bases, component_managers=component_managers, component_organizer=component_organizer, annotation_mapping=annotation_mapping, operators_visitors=operators_visitors)

        super(MonkeyMeta, cls).__init__(name, bases, attrs)

        monkey_bases = [base for base in bases if type(base) == MonkeyMeta]
        logger.info(f"Monkey Bases = {monkey_bases}", extra={STAGE: "META SETUP", MONKEY: name})

        for component_manager in cls.__component_managers__:
            component_manager.build(cls, monkey_bases, attrs)

        model_components = attrs[NamespacesConsts.COMPONENTS]
        logger.info(f"Post Component Managers All Model Components = {model_components}", extra={STAGE: "Component Info", MONKEY: name})
        cls.__organized_components__ = cls.__component_organizer__.order_by_chain_of_responsibility(model_components)
        logger.info(f"Post Component Managers Organized Model Components = {cls.__organized_components__}", extra={STAGE: "Component Info", MONKEY: name})

        for component_type, components in cls.__organized_components__.items():
            for component in components:
                component.validate(cls, bases, attrs)

        rules_exception: RulesException = attrs[NamespacesConsts.EXCEPTIONS]
        if not rules_exception.is_empty():
            raise rules_exception

        for component_type, components in cls.__organized_components__.items():
            for component in components:
                component.build(cls, bases, attrs)

        logger.info(f"Post Components Build Organized Model Components = {cls.__organized_components__}", extra={STAGE: "Component Info", MONKEY: name})

        cls.__organized_components__ = cls.__component_organizer__.order_for_instance_operation(cls, cls.__organized_components__)
        logger.info(f"Model Components Run Order:", extra={STAGE: "Component Info", MONKEY: name})

        for component in cls.__organized_components__:
            scope = getattr(component, ComponentConsts.FIELD_KEY, ComponentConsts.GLOBAL)
            logger.info(f"{component} -> {scope}", extra={STAGE: "Component Info", MONKEY: name})


