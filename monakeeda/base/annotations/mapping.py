from typing import Type, TypeVar

from monakeeda.helpers import defaultdictvalue
from .base_annotations import Annotation, GenericAnnotation
from .annotations import TypeVarAnnotation, ArbitraryAnnotation
# from .errors import NotAnAnnotationException
from .helpers import get_type_cls


class AnnotationDefaultDict(defaultdictvalue):

    def __getitem__(self, type_):
        gotten = super(AnnotationDefaultDict, self).__getitem__(get_type_cls(type_))
        return gotten

    def __setitem__(self, key, item):
        if isinstance(item, TypeVar):  # item and key will be the same on TypeVars
            super(AnnotationDefaultDict, self).__setitem__(key, TypeVarAnnotation)
        elif issubclass(item.mro()[0], Annotation):
            super(AnnotationDefaultDict, self).__setitem__(key, item)
        else:
            super(AnnotationDefaultDict, self).__setitem__(key, ArbitraryAnnotation)
            # raise NotAnAnnotationException(key)


annotation_mapping = {}
annotation_mapping = AnnotationDefaultDict(lambda annotation: annotation, annotation_mapping)


def annotation_mapper(*key_annotations: Type, annotation_mapping=annotation_mapping):
    def inner_get_annotation_cls(annotation_cls: Type[Annotation]):
        for key_annotation in key_annotations:
            annotation_mapping[key_annotation] = annotation_cls

        return annotation_cls

    return inner_get_annotation_cls


def get_generics_annotations(annotation: GenericAnnotation):
    annotations = []

    for t in annotation._types:
        if t != type(None):
            annotations.append(annotation_mapping[t](annotation._field_key, t))

    return annotations

