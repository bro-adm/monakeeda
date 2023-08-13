from typing import Type, List

from monakeeda.helpers import defaultdictvalue
from .base_annotation import Annotation
from .errors import NotAnAnnotationException
from .helpers import get_type_cls


class AnnotationDefaultDict(defaultdictvalue):

    def __getitem__(self, type_):
        gotten = super(AnnotationDefaultDict, self).__getitem__(get_type_cls(type_))
        return gotten(type_)

    def __setitem__(self, key, item):
        if issubclass(item.mro()[0], Annotation):
            super(AnnotationDefaultDict, self).__setitem__(key, item)
        else:
            raise NotAnAnnotationException(key)


annotation_mapping = {}
annotation_mapping = AnnotationDefaultDict(lambda annotation: annotation, annotation_mapping)


def annotation_mapper(key_annotations: List[Type], annotation_mapping=annotation_mapping):
    def inner_get_annotation_cls(annotation_cls: Type[Annotation]):
        for key_annotation in key_annotations:
            annotation_mapping[key_annotation] = annotation_cls

        return annotation_cls

    return inner_get_annotation_cls
