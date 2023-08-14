from .helpers import ignore_unwanted_params
from ..annotations import AnnotationMainComponent, annotation_mapping, ModelAnnotation
from ..component import ComponentInitComposite
from ..config import ConfigMainComponent, Config
from ..decorators import DecoratorMainComponent
from ..fields import FieldMainComponent
from ..meta import MonkeyMeta

# TODO: create signature component
model_components = \
    ComponentInitComposite(
        FieldMainComponent(),
        DecoratorMainComponent(),
        AnnotationMainComponent(annotation_mapping),
        ConfigMainComponent()
    )


# TODO: add update method and dict/view method
class MonkeyModel(metaclass=MonkeyMeta, model_components=model_components, annotation_mapping=annotation_mapping):

    def __init__(self, **kwargs):
        for key in self.__map__['main_field_keys']:
            kwargs = self.__model_components__.values_handler(key, self, kwargs)
        kwargs = ignore_unwanted_params(self.__class__, kwargs)
        for key in kwargs:
            super(MonkeyModel, self).__setattr__(key, kwargs[key])
        # The super setter because the setter logic can be changed and in teh init we have data as we want it already

    def __init_subclass__(cls):
        # can't put the start of __map__ here because the set_cls_namespace happens before in the meta cls
        cls.__annotation_mapping__[cls] = ModelAnnotation

    # this is for run debug purposes.
    def __repr__(self):
        return str(self.__dict__)

    class Config(Config):
        pass
