from typing import Any

from monakeeda.consts import NamespacesConsts
from monakeeda.utils import deep_update, exclude_keys
from ..component import Stages
from ..fields import FieldManager
from ..annotations import AnnotationManager, annotation_mapping, ModelAnnotation
from ..decorators import DecoratorManager
from ..config import ConfigManager, Config
from ..meta import MonkeyMeta
from ..operator import all_operators
from .errors import MonkeyValuesHandlingException

component_managers = [FieldManager(), AnnotationManager(annotation_mapping), DecoratorManager(), ConfigManager()]


class BaseModel(metaclass=MonkeyMeta, component_managers=component_managers, annotation_mapping=annotation_mapping, operators_visitors=all_operators):

    def __init_subclass__(cls):
        super().__init_subclass__()
        # can't put the start of __map__ here because the set_cls_namespace happens before in the meta cls
        cls.__annotation_mapping__[cls] = ModelAnnotation

    @classmethod
    def struct(cls) -> dict:
        return getattr(cls, NamespacesConsts.STRUCT).copy()

    def _handle_values(self, values: dict, stage):
        exceptions = []  # pass by reference - so updates will be available
        super(BaseModel, self).__setattr__(NamespacesConsts.EXCEPTIONS, exceptions)
        # this is an instance level field as opposed to the class level exceptions list used in the build phase

        for component_type, components in self.__organized_components__.items():
            for component in components:
                component.handle_values(self, values, stage)

        if exceptions:
            raise MonkeyValuesHandlingException(self.__class__.__name__, values, exceptions)

        for key in values:
            super(BaseModel, self).__setattr__(key, values[key])
        # The super setter because the setter logic can be changed and in teh init we have data as we want it already

    def __init__(self, **kwargs):
        self._handle_values(kwargs, Stages.INIT)
        # The super setter because the setter logic can be changed and in teh init we have data as we want it already

    def update(self, **kwargs):
        kwargs = deep_update(self.__dict__.copy(), kwargs)
        self._handle_values(kwargs, Stages.UPDATE)

    def __setattr__(self, key, value):
        self.update(**{key: value})

    @staticmethod
    def _operate(model, operator_type: str, context: Any):
        operator_visitor = model.__operators_visitors__[operator_type]

        for component_type, components in model.__organized_components__.items():
            for component in components:
                component.accept_operator(operator_visitor, context)

    # this is for run debug purposes.
    def __repr__(self):
        the_dict = exclude_keys(self.__dict__, [NamespacesConsts.EXCEPTIONS])
        return str(the_dict)

    class Config(Config):
        pass
