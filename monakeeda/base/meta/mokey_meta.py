from abc import ABCMeta
from collections import OrderedDict

from monakeeda.base.component import RulesException
from monakeeda.consts import NamespacesConsts


class MonkeyMeta(ABCMeta):
    def __new__(mcs, name, bases, attrs, **_):
        cls = super(MonkeyMeta, mcs).__new__(mcs, name, bases, attrs)
        return cls

    def __init__(cls, name, bases, attrs, model_components=None, annotation_mapping=None):
        if not bases:
            if model_components == None or annotation_mapping == None:
                raise ValueError('direct metaclass users needs to pass the model_components and annotation_mapping')
            cls.__model_components__ = model_components
            cls.__annotation_mapping__ = annotation_mapping
        else:
            cls.__model_components__ = model_components if model_components else bases[0].__model_components__
            cls.__annotation_mapping__ = annotation_mapping if annotation_mapping else bases[0].__annotation_mapping__

        super(MonkeyMeta, cls).__init__(name, bases, attrs)

        cls.__map__ = {NamespacesConsts.BUILD: {}, NamespacesConsts.FIELDS: OrderedDict()}

        # TODO: think about how to make landscape not hard coded logic
        attrs[NamespacesConsts.BUILD][NamespacesConsts.EXCEPTIONS] = RulesException(name, [])
        if cls.__model_components__.build(cls, bases, attrs):
            raise attrs[NamespacesConsts.BUILD][NamespacesConsts.EXCEPTIONS]
