from typing import Any, TypeVar

from monakeeda.base import MonkeyBuilder, Annotation, Component, ExceptionsDict, GenericAnnotation
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
    Say i am an annotation or a field parameter and i have a logic that only works on a specific annotation type.
    Specific annotation requirements can a BaseModel, a str, a int/float (and their inheriting classes) up to some generics (e.g. Discriminator/Union/Const)

    Here you give the core annotation you support and if the user set a valid annotation it sets the _core_types attr of the main Component.
    e.g. I asked for a BaseModel and you set a CustomModel annotation -> the _core_types will be the CustomModel
    e.g. I asked for a BaseModel and you set a str -> raises error
    e.g. I asked for a BaseModel and you set a Const[CustomModel] -> the _core_types will be the CustomModel
    e.g. I asked for a BaseModel and you set a Union[CustomModel1, Const[CustomModel2]] ->  the _core_types will be the [CustomModel1, CustomModel2]
    e.g. I ask for int/float and you provide Const[Cast[int]] -> returns int
    e.g. I ask for Cast and you provide Const[Cast[int]] -> returns Cast[int]
    """

    def __init__(self, *supported_core_annotations: Any):
        self.supported_core_annotations = supported_core_annotations

    def _generic_annotation_extraction(self, supported_annotation: Annotation, set_annotation: Annotation):
        sub_annotations = supported_annotation._annotations
        if sub_annotations:  # not only the generic -> also has subtype requirements
            raise NotImplemented  # not implemented subtype requirements validation -> what does it even mean

        if isinstance(set_annotation, supported_annotation.__class__):
            return set_annotation.set_annotation

        if isinstance(set_annotation, GenericAnnotation):
            sub_annotations = set_annotation.represented_annotations
            if len(sub_annotations) == 1:
                return self._generic_annotation_extraction(supported_annotation, sub_annotations[0])

        return False  # not a match

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder: Component):
        main_builder._core_types = None

        set_annotation: Annotation = monkey_cls.struct[NamespacesConsts.ANNOTATIONS][main_builder.scope]  # if not field key will raise error
        annotations_mapping = set_annotation._annotations_mapping

        supported_annotations = []
        for core_annotation in self.supported_core_annotations:
            annotations_mapping[core_annotation]
            annotation = annotations_mapping[core_annotation](set_annotation.scope, core_annotation, annotations_mapping)
            supported_annotations.append(annotation)

        supported_core_annotations = []
        for supported_annotation in supported_annotations:
            if isinstance(supported_annotation, GenericAnnotation):
                result = self._generic_annotation_extraction(supported_annotation, set_annotation)
                if result:
                    main_builder._core_types = (result, )
                    break
            else:
                supported_core_annotations.extend(wrap_in_list(supported_annotation.represented_types))

        if not main_builder._core_types:
            if not supported_core_annotations:
                # exception for the case where provided with support for only Generic Types and no match was found
                exception = CoreAnnotationNotAllowedException(main_builder, self.supported_core_annotations, set_annotation.set_annotation)
                exceptions[main_builder.scope].append(exception)

            else:  # try match for supported non-generic annotations via core api
                set_core_annotations = wrap_in_list(set_annotation.represented_types)

                for core_annotation in set_core_annotations:
                    if not isinstance(core_annotation, TypeVar) and not issubclass(core_annotation, tuple(supported_core_annotations)):
                        exception = CoreAnnotationNotAllowedException(main_builder, supported_core_annotations, set_core_annotations)
                        exceptions[main_builder.scope].append(exception)
                        break

                main_builder._core_types = set_core_annotations
