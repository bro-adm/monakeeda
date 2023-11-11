from abc import ABCMeta

from monakeeda.consts import NamespacesConsts
from ..component import RulesException
from .helpers import handle_class_inputs


class MonkeyMeta(ABCMeta):
    def __new__(mcs, name, bases, attrs, **_):
        attrs[NamespacesConsts.STRUCT] = {}
        attrs[NamespacesConsts.COMPONENTS] = []
        attrs[NamespacesConsts.EXCEPTIONS] = RulesException(name, [])
        attrs[NamespacesConsts.TMP] = {}

        cls = super(MonkeyMeta, mcs).__new__(mcs, name, bases, attrs)
        return cls

    def __init__(cls, name, bases, attrs, component_managers=None, component_organizer=None, annotation_mapping=None, operators_visitors=None):
        print("###################")
        print(name, bases)

        handle_class_inputs(cls, bases, component_managers=component_managers, component_organizer=component_organizer, annotation_mapping=annotation_mapping, operators_visitors=operators_visitors)

        super(MonkeyMeta, cls).__init__(name, bases, attrs)

        monkey_bases = [base for base in bases if type(base) == MonkeyMeta]

        for component_manager in cls.__component_managers__:
            component_manager.build(cls, monkey_bases, attrs)

        model_components = attrs[NamespacesConsts.COMPONENTS]
        cls.__organized_components__ = cls.__component_organizer__.order_by_chain_of_responsibility(model_components)

        for component_type, components in cls.__organized_components__.items():
            for component in components:
                component.validate(cls, bases, attrs)

        rules_exception: RulesException = attrs[NamespacesConsts.EXCEPTIONS]
        if not rules_exception.is_empty():
            raise rules_exception

        for component_type, components in cls.__organized_components__.items():
            for component in components:
                component.build(cls, bases, attrs)

        cls.__organized_components__ = cls.__component_organizer__.order_for_instance_operation(cls, cls.__organized_components__)

        print("---------------------------")

        for key, val in cls.struct.items():
            print(key, val)

        print("------------------------------")

        for component in cls.__organized_components__:
            print(type(component), getattr(component, '_field_key', 'global'))

        print("------------------------------")
