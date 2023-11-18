from abc import ABCMeta
from typing import Type, TypeVar

from monakeeda.helpers import defaultdictvalue
from .base_annotations import Annotation, GenericAnnotation
from .helpers import get_type_cls
from .known_annotations import known_annotations, KnownAnnotations


class AnnotationDefaultDict(defaultdictvalue):

    def __init__(self, default_factory, init_value, known_annotations=known_annotations):
        super().__init__(default_factory, init_value)
        self._known_annotations = known_annotations

    def __getitem__(self, type_):
        """
        Gets the uses set annotations -> calls get_type_cls to get the "native" typing/cls annotation.
        Calls super getitem which has the defaultdict logic of missing keys which itself calls the setitem logic.

        The final output will be a Monakeeda Annotation Cls.
        """

        gotten = super(AnnotationDefaultDict, self).__getitem__(get_type_cls(type_))
        return gotten

    def __setitem__(self, key, item):
        """
        This method is either called on by an asked for setitem or by a missing getitem.

        The key is the client set annotation.
        The item is default_factory result (missing getitem) or a directly provided Annotation (setitem) - if configured as intended.

        Examples on the case default_factory = lambda x: x (key, item):
            - str, StrAnnotation (setitem)
            - Cast, Cast (missing getitem)
            - CustomModel, CustomModel (missing getitem)
            - ~TypeVar, ~TypeVar (missing getitem)
            - CustomCls, CustomCls (missing getitem)

        Maps them together accordingly to custom Monakeeda Annotations.

        The goal is to map the given key to the implemented Annotation for the received item.
            - CustomModel -> ModelAnnotation
            - StrAnnotation -> StrAnnotation
            - ~TypeVar -> TypeVarAnnotation

        The known scopes of this mapping is the Annotation Cls.
        All other mappings are provided via KnownAnnotations that we do not want to use directly for the following reasons:
            - Allow overrides
            - Implement them in the Implementations dir to keep consistency of __prior_handler__ usage and not be bugged down by python import logic (that we so nicelly use to our advantage)

        """

        if item.__class__ == ABCMeta and issubclass(item, Annotation):  # issubclass must get a cls type -> instance cls will be the actual cls
            super(AnnotationDefaultDict, self).__setitem__(key, item)
        else:
            # We are in the realm of missing items -> key will be the user set annotation and item the result of the default_factory func
            for known_type, type_info in self._known_annotations.items():
                base_type, is_type_func, annotation_cls = type_info

                if is_type_func(item, base_type):
                    super(AnnotationDefaultDict, self).__setitem__(key, annotation_cls)
                    break


annotation_mapping = {}
annotation_mapping = AnnotationDefaultDict(lambda annotation: annotation, annotation_mapping)


def annotation_mapper(*key_annotations: Type, annotation_mapping=annotation_mapping):
    def inner_get_annotation_cls(annotation_cls: Type[Annotation]):
        for key_annotation in key_annotations:
            annotation_mapping[key_annotation] = annotation_cls

        return annotation_cls

    return inner_get_annotation_cls


def get_generics_annotations(annotation: GenericAnnotation):
    """
    Returns the Monakeeda Annotations of each of the generics set in the GenericAnnotation.

    Used to usually run them as next handlers in handle_values
    """

    annotations = []

    for t in annotation._types:
        if t != type(None):
            annotations.append(annotation_mapping[t](annotation._field_key, t))

    return annotations
