from typing import Any, TypeVar

from monakeeda.base import MonkeyBuilder, Annotation, Component, ExceptionsDict
from monakeeda.consts import NamespacesConsts
from monakeeda.utils import wrap_in_list


class CoreAnnotationNotAllowedException(Exception):
    def __init__(self, component: Component, core_annotation, provided_annotation):
        self.component_representor = component.representor
        self.core_annotation = core_annotation
        self.provided_annotation = provided_annotation

    def __str__(self):
        return f"{self.component_representor} supports core annotation {self.core_annotation} but was provided with {self.provided_annotation}."


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

    def __init__(self, *supported_core_annotations: Any):
        self.supported_core_annotations = supported_core_annotations

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder: Component):
        set_annotation: Annotation = monkey_cls.struct[NamespacesConsts.ANNOTATIONS][main_builder.scope]  # if not field key will raise error
        set_core_annotations = wrap_in_list(set_annotation.core_types)

        annotations_mapping = set_annotation._annotations_mapping
        supported_annotations = []
        for core_annotation in self.supported_core_annotations:
            annotations_mapping[core_annotation]
            annotation = annotations_mapping[core_annotation](set_annotation.scope, core_annotation, annotations_mapping)
            supported_annotations.append(annotation)
        supported_core_annotations = [wrap_in_list(annotation.core_types) for annotation in supported_annotations]

        is_error = False

        for core_annotation in set_core_annotations:
            for supported_annotation_set in supported_core_annotations:
                if not isinstance(core_annotation, TypeVar) and not issubclass(core_annotation, tuple(supported_annotation_set)):
                    is_error = True
                    break

            if is_error:
                break

        if is_error:
            exception = CoreAnnotationNotAllowedException(main_builder, supported_core_annotations, set_core_annotations)
            exceptions[main_builder.scope].append(exception)

        main_builder._core_types = set_core_annotations
