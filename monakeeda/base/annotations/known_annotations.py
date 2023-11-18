from collections import OrderedDict
from enum import Enum
from typing import Type

from .base_annotations import Annotation

"""
One of Monakeeda's ideologies requires us to make anything and everything overrideable.

In the case of Annotations, a user gets to set python native and monakeeda native annotations when setting a monkey.
Some of these annotations are not directly Annotations implementations, nor are they mapped to an actual Annotation.

The types listed below are the types that ring true the the above claims.

The compartment responsible for mapping client set annotations to Annotation implementations is the annotations_mapping.
We could just implement the Annotations here and hard map them to each of our client set annotations.
But as you may understand that wouldn't be client overridable, so this is the solution.

Not to mention it actually helps us in using the __prior_handler__ on all native components,
And allows non issues when importing and setting the chain of responsibility order.
"""


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
