from typing import Any, _TYPING_INTERNALS

from monakeeda.consts import NamespacesConsts, TmpConsts
from monakeeda.utils import deep_update
from monakeeda.logger import logger, STAGE, MONKEY
from .base_components_organizer import BaseComponentsOrganizer
from .errors import MonkeyValuesHandlingException
from .generic_alias import MonkeyGenericAlias
from ..annotations import AnnotationManager, annotation_mapping, ModelAnnotation
from ..config import ConfigManager
from ..decorators import DecoratorManager
from ..fields import FieldManager
from ..interfaces import Stages
from ..meta import MonkeyMeta
from ..operator import all_operators

component_managers = [ConfigManager(), FieldManager(), DecoratorManager(), AnnotationManager(annotation_mapping)]


class BaseModel(metaclass=MonkeyMeta, component_managers=component_managers, component_organizer=BaseComponentsOrganizer(), annotation_mapping=annotation_mapping, operators_visitors=all_operators):
    """
    Responsible for holding the PURE run of all the logics combined without being dependent on any specific compartment.

    Supplies the API for further extensions (e.g. _operate)

    Also Responsible for managing python's weird shticks (e.g. generics -> __class_getitem__)
    """

    def __init_subclass__(cls):
        super().__init_subclass__()
        # can't put the start of __map__ here because the set_cls_namespace happens before in the meta cls
        cls.__annotation_mapping__[cls] = ModelAnnotation

    def __class_getitem__(cls, item):
        generic = super().__class_getitem__(item)  # probably will only be called when actually Generic
        getattr(cls, NamespacesConsts.TMP)[TmpConsts.GENERICS] = generic.__args__

        logger.info(f"Class Scope Generics = {generic.__args__}", extra={STAGE: "Monkey Generics", MONKEY: cls.__name__})

        return MonkeyGenericAlias.init_from_typing_generic_alias(generic)

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

        if exceptions:
            raise MonkeyValuesHandlingException(self.__class__.__name__, values, exceptions)

        for key in values:
            super(BaseModel, self).__setattr__(key, values[key])

    def __init__(self, **kwargs):
        self._handle_values(kwargs, Stages.INIT)

    def update(self, **kwargs):
        logger.info(f"Update Scope Generics = {self.__orig_class__.__args__}", extra={STAGE: "Monkey Generics", MONKEY: self.__class__.__name__})

        kwargs = deep_update(self.__dict__.copy(), kwargs)
        self._handle_values(kwargs, Stages.UPDATE)

    def __setattr__(self, key, value):
        if key in _TYPING_INTERNALS:  # Python's weird usage of inheritance with generics and their initialization
            super().__setattr__(key, value)
        else:
            self.update(**{key: value})

    @staticmethod
    def _operate(model, operator_type: str, context: Any):
        operator_visitor = model.__operators_visitors__[operator_type]

        for component in model.__organized_components__:
            component.accept_operator(operator_visitor, context)
