from typing import Any, get_origin, get_args, Union

from monakeeda.base import Parameter, MonkeyBuilder, Annotation
from monakeeda.consts import NamespacesConsts
from monakeeda.helpers import ExceptionsDict


class CoreAnnotationNotAllowedException(Exception):
    def __init__(self, component: str, core_annotation, provided_annotation):
        self.component = component
        self.core_annotation = core_annotation
        self.provided_annotation = provided_annotation

    def __str__(self):
        return f"{self.component} supports core annotation {self.core_annotation} but was provided with {self.provided_annotation}."


class CoreAnnotationsExtractor(MonkeyBuilder):
    """
    Say i aam an annotation or a field parameter and i have a logic that only works on a specific annotation type.
    That specific annotation can be from a BaseModel and a str (and their inheriting classes) up to Union[str, int] and other infinite generic types.

    Here you give the core annotation you support and if the user set a valid annotation it sets the _core_types attr of the main Component.
    e.g. I asked for a BaseModel and you set a CustomModel annotation -> the _core_types will be the CustomModel
    e.g. I asked for a BaseModel and you set a str -> raises error
    e.g. I asked for a BaseModel and you set a Const[CustomModel] -> the _core_types will be the CustomModel
    e.g. I asked for a BaseModel and you set a Union[CustomModel1, Const[CustomModel2]] ->  the _core_types will be the [CustomModel1, CustomModel2]

    CURRENTLY DOES NOT SUPPORT MULTI CORE TYPES
    """

    def __init__(self, core_annotation: Any):
        self.core_annotation = core_annotation

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder: Union[Annotation, Parameter]):
        set_annotation = monkey_cls.struct[NamespacesConsts.ANNOTATIONS][main_builder._field_key]
        annotations_mapping = set_annotation._annotations_mapping

        if isinstance(main_builder, Annotation):
            annotation_origin = get_origin(main_builder.base_type)
            self.core_annotation = annotation_origin[self.core_annotation]
            component_identifier = main_builder.__class__.__name__
        else:
            component_identifier = main_builder.__key__

        annotations_mapping[self.core_annotation]
        supported_annotation = annotations_mapping[self.core_annotation](set_annotation._field_key, self.core_annotation, annotations_mapping)

        result = supported_annotation.is_same(set_annotation)
        if not result:
            exception = CoreAnnotationNotAllowedException(component_identifier, self.core_annotation, set_annotation.base_type)
            exceptions[main_builder._field_key].append(exception)

        if isinstance(main_builder, Annotation):
            main_builder._core_types = get_args(result)
        else:
            main_builder._core_types = result if type(result)==tuple else (result, )
