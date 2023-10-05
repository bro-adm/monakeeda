from abc import ABCMeta
from collections import OrderedDict

from monakeeda.consts import NamespacesConsts
from ..component import RulesException, organize_components


class MonkeyMeta(ABCMeta):
    def __new__(mcs, name, bases, attrs, **_):
        attrs.setdefault(NamespacesConsts.MAP, {NamespacesConsts.COMPONENTS: [], NamespacesConsts.BUILD: {}, NamespacesConsts.FIELDS: OrderedDict()})
        attrs[NamespacesConsts.MAP][NamespacesConsts.BUILD][NamespacesConsts.EXCEPTIONS] = RulesException(name, [])

        cls = super(MonkeyMeta, mcs).__new__(mcs, name, bases, attrs)
        return cls

    def __init__(cls, name, bases, attrs, component_managers=None, annotation_mapping=None, operators_visitors=None):
        if not bases:
            if component_managers == None or annotation_mapping == None and operators_visitors == None:
                raise ValueError('direct metaclass users needs to pass the model_components, annotation_mapping, operators_visitors')
            cls.__component_managers__ = component_managers
            cls.__annotation_mapping__ = annotation_mapping
            cls.__operators_visitors__ = operators_visitors
        else:
            cls.__component_managers__ = component_managers if component_managers else bases[0].__component_managers__
            cls.__annotation_mapping__ = annotation_mapping if annotation_mapping else bases[0].__annotation_mapping__
            cls.__operators_visitors__ = operators_visitors if operators_visitors else bases[0].__operators_visitors__

        super(MonkeyMeta, cls).__init__(name, bases, attrs)

        for component_manager in cls.__component_managers__:
            component_manager.build(cls, bases, attrs)

        model_components = cls.__map__[NamespacesConsts.COMPONENTS]
        cls.__organized_components__ = organize_components(model_components)

        # print(name)
        # print(cls.__organized_components__)
        # print(cls.__map__[NamespacesConsts.FIELDS])
        # print(cls.__map__[NamespacesConsts.BUILD])
        # print(cls.__map__[NamespacesConsts.COMPONENTS])
        # print('------------------------------------------')

        for component_type, components in cls.__organized_components__.items():
            for component in components:
                component.validate(cls, bases, attrs)

        rules_exception: RulesException = cls.__map__[NamespacesConsts.BUILD][NamespacesConsts.EXCEPTIONS]
        if not rules_exception.is_empty():
            raise rules_exception

        for component_type, components in cls.__organized_components__.items():
            for component in components:
                component.build(cls, bases, attrs)
