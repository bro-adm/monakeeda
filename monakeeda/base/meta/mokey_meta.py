from abc import ABCMeta
from collections import defaultdict

from monakeeda.consts import NamespacesConsts
from monakeeda.logger import logger, STAGE, MONKEY
from .errors import MonkeyBuildException
from .helpers import handle_class_inputs
from ..scope import ScopeDict
from ..exceptions_manager import ExceptionsDict


class MonkeyMeta(ABCMeta):
    """
    __new__ sets initial monkey landscapes.

    __init__ sets the configurators of this class (via override or inheritance) and then runs them:
        - ComponentManagers
        - ComponentsOrganizer
        - Components Validations & Builds
        - ComponentsOrganizer

    After these logics run (can be a little heavy) your monkey cls is available to use.
    These are one time logics that happen in load/import time.
    """

    def __new__(mcs, name, bases, attrs, **_):
        attrs[NamespacesConsts.STRUCT] = {}
        attrs[NamespacesConsts.SCOPES] = defaultdict(lambda: ScopeDict(), {})
        attrs[NamespacesConsts.COMPONENTS] = []
        attrs[NamespacesConsts.TMP] = {}

        logger.info(f"Bases = {bases}", extra={STAGE: "META SETUP", MONKEY: name})
        logger.info(f"Attrs = {attrs}", extra={STAGE: "META SETUP", MONKEY: name})

        cls = super(MonkeyMeta, mcs).__new__(mcs, name, bases, attrs)
        return cls

    def __init__(cls, name, bases, attrs, component_managers=None, scopes_manager=None, component_organizer=None, operators_visitors=None):
        handle_class_inputs(cls, bases, component_managers=component_managers, scopes_manager=scopes_manager, component_organizer=component_organizer, operators_visitors=operators_visitors)

        super(MonkeyMeta, cls).__init__(name, bases, attrs)

        monkey_bases = [base for base in bases if type(base) == MonkeyMeta]
        logger.info(f"Monkey Bases = {monkey_bases}", extra={STAGE: "META SETUP", MONKEY: name})

        for component_manager in cls.__component_managers__:
            component_manager.build(cls, monkey_bases, attrs, {})

        model_components = attrs[NamespacesConsts.COMPONENTS]
        logger.info(f"Post Component Managers All Model Components = {model_components}", extra={STAGE: "Component Info", MONKEY: name})
        cls.__type_organized_components__ = cls.__component_organizer__.order_by_chain_of_responsibility(model_components)
        logger.info(f"Post Component Managers Organized Model Components = {cls.__type_organized_components__}", extra={STAGE: "Component Info", MONKEY: name})

        build_exceptions = ExceptionsDict()
        for component_type, components in cls.__type_organized_components__.items():
            for component in components:
                component.build(cls, bases, attrs, build_exceptions)

        cls.__scopes_manager__.build(cls, bases, attrs, build_exceptions)

        if build_exceptions:
            raise MonkeyBuildException(name, build_exceptions)

        logger.info(f"Post Components Build Organized Model Components = {cls.__type_organized_components__}", extra={STAGE: "Component Info", MONKEY: name})
        logger.info(f"Scopes = {attrs[NamespacesConsts.SCOPES]}", extra={STAGE: "Component Info", MONKEY: name})

        cls.__run_organized_components__ = cls.__component_organizer__.order_for_instance_operation(cls, cls.__type_organized_components__)
        logger.info(f"Model Components Run Order:", extra={STAGE: "Component Info", MONKEY: name})

        for component in cls.__run_organized_components__:
            logger.info(f"\t{component} -> {component.scope}", extra={STAGE: "Component Info", MONKEY: name})
