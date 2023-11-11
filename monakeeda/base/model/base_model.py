from typing import Any, _TYPING_INTERNALS, _GenericAlias, Generic

from monakeeda.consts import NamespacesConsts, TmpConsts
from monakeeda.utils import deep_update
from ..component import Stages
from ..fields import FieldManager
from ..annotations import AnnotationManager, annotation_mapping, ModelAnnotation
from ..decorators import DecoratorManager
from ..config import ConfigManager, Config
from ..meta import MonkeyMeta
from ..operator import all_operators
from .errors import MonkeyValuesHandlingException
from .basic_organizer import BaseComponentOrganizer
from .generic_alias import MonkeyGenericAlias

component_managers = [ConfigManager(), FieldManager(), DecoratorManager(), AnnotationManager(annotation_mapping)]


class BaseModel(metaclass=MonkeyMeta, component_managers=component_managers, component_organizer=BaseComponentOrganizer(), annotation_mapping=annotation_mapping, operators_visitors=all_operators):

    def __init_subclass__(cls):
        super().__init_subclass__()
        # can't put the start of __map__ here because the set_cls_namespace happens before in the meta cls
        cls.__annotation_mapping__[cls] = ModelAnnotation

    def __class_getitem__(cls, item):
        generic = super().__class_getitem__(item)  # probably will only be called when actually Generic

        getattr(cls, NamespacesConsts.TMP)[TmpConsts.GENERICS] = generic.__args__

        mok = MonkeyGenericAlias.init_from_typing_generic_alias(generic)
        return mok

    @classmethod
    @property
    def struct(cls) -> dict:
        return getattr(cls, NamespacesConsts.STRUCT)

    def _handle_values(self, values: dict, stage):
        exceptions = []  # pass by reference - so updates will be available
        super(BaseModel, self).__setattr__(NamespacesConsts.EXCEPTIONS, exceptions)
        # this is an instance level field as opposed to the class level exceptions list used in the build phase

        for component in self.__organized_components__:
            component.handle_values(self, values, stage)
            # print(component, exceptions)

        if exceptions:
            raise MonkeyValuesHandlingException(self.__class__.__name__, values, exceptions)

        for key in values:
            super(BaseModel, self).__setattr__(key, values[key])
        # The super setter because the setter logic can be changed and in teh init we have data as we want it already

    def __init__(self, **kwargs):
        self._handle_values(kwargs, Stages.INIT)
        # not set in actual init because python typing shit happens there ALWAYS after custom init logic.
        # that shit is needed to run the actual init logic for generics :(

    def update(self, **kwargs):
        kwargs = deep_update(self.__dict__.copy(), kwargs)
        self._handle_values(kwargs, Stages.UPDATE)

    def __setattr__(self, key, value):
        if key in _TYPING_INTERNALS:  # F Python and its weird usage of inheritence with generics and their initalization
            super().__setattr__(key, value)
        else:
            self.update(**{key: value})

    @staticmethod
    def _operate(model, operator_type: str, context: Any):
        operator_visitor = model.__operators_visitors__[operator_type]

        for component_type, components in model.__organized_components__.items():
            for component in components:
                component.accept_operator(operator_visitor, context)
