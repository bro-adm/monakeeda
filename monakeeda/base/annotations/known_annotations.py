from collections import OrderedDict
from enum import Enum
from typing import Type

from .base_annotations import Annotation


class KnownAnnotations(Enum):
    ModelAnnotation = 'ModelAnnotation'
    TypeVarAnnotation = 'TypeVarAnnotation'
    ArbitraryAnnotation = 'ArbitraryAnnotation'


known_annotations = OrderedDict()


def known_annotation_mapper(known_type: KnownAnnotations, base_type: type, is_type_func, known_annotations=known_annotations):
    def inner_get_known_annotation(annotation_cls: Type[Annotation]):
        known_annotations[known_type] = (base_type, is_type_func, annotation_cls)

        return annotation_cls

    return inner_get_known_annotation
