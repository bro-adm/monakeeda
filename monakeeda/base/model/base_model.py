from ..annotations import AnnotationMainComponent, annotation_mapping, ModelAnnotation
from ..component import MainComponentInitComposite, Stages
from ..config import ConfigMainComponent, Config
from ..decorators import DecoratorMainComponent
from ..fields import FieldMainComponent
from ..meta import MonkeyMeta
from ...utils import deep_update

model_components = MainComponentInitComposite([FieldMainComponent(), DecoratorMainComponent(), AnnotationMainComponent(annotation_mapping), ConfigMainComponent()])


class MonkeyModel(metaclass=MonkeyMeta, model_components=model_components, annotation_mapping=annotation_mapping, priority=5):

    def _values_handler(self, values: dict, stage):
        for i in range(self.__priority__):  # includes 0
            kwargs = self.__model_components__.values_handler(i, self, values, stage)
            values.update(kwargs)

        # kwargs = ignore_unwanted_params(self.__class__, kwargs)

        for key in values:
            super(MonkeyModel, self).__setattr__(key, values[key])
        # The super setter because the setter logic can be changed and in teh init we have data as we want it already

    def __init__(self, **kwargs):
        self._values_handler(kwargs, Stages.INIT)
        # The super setter because the setter logic can be changed and in teh init we have data as we want it already

    def update(self, **kwargs):
        kwargs = deep_update(self.__dict__.copy(), kwargs)
        self._values_handler(kwargs, Stages.UPDATE)

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
