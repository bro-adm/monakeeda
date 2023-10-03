from ..component import Stages
from ..fields import FieldManager
from ..annotations import AnnotationManager, annotation_mapping, ModelAnnotation
from ..config import ConfigManager, Config
from ..meta import MonkeyMeta
from ...utils import deep_update

component_managers = [FieldManager(), AnnotationManager(annotation_mapping), ConfigManager()]


class MonkeyModel(metaclass=MonkeyMeta, component_managers=component_managers, annotation_mapping=annotation_mapping):

    def _handle_values(self, values: dict, stage):
        for component_type, components in self.__organized_components__.items():
            for component in components:
                kwargs = component.handle_values(self, values, stage)
                values.update(kwargs)

        # kwargs = ignore_unwanted_params(self.__class__, kwargs)

        for key in values:
            super(MonkeyModel, self).__setattr__(key, values[key])
        # The super setter because the setter logic can be changed and in teh init we have data as we want it already

    def __init__(self, **kwargs):
        self._handle_values(kwargs, Stages.INIT)
        # The super setter because the setter logic can be changed and in teh init we have data as we want it already

    def update(self, **kwargs):
        kwargs = deep_update(self.__dict__.copy(), kwargs)
        self._handle_values(kwargs, Stages.UPDATE)

    def __setattr__(self, key, value):
        self.update(**{key: value})

    def __init_subclass__(cls):
        # can't put the start of __map__ here because the set_cls_namespace happens before in the meta cls
        cls.__annotation_mapping__[cls] = ModelAnnotation

    # this is for run debug purposes.
    def __repr__(self):
        return str(self.__dict__)

    class Config(Config):
        pass
