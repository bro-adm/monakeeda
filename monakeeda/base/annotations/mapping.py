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
        As seen above and in the helper funcs, this method gets:
            - key = python native type / typing annotation / Monakeeda annotation cls / any cls
            - item = Monakeeda Annotation / TypeVar / any cls

        Maps them together accordingly to custom Monakeeda Annotations.

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


        # if isinstance(item, TypeVar):  # item and key will be the same on TypeVars
        #     _TypeVarAnnotation = self._known_annotations[KnownAnnotations.TypeVarAnnotation]
        #     super(AnnotationDefaultDict, self).__setitem__(key, _TypeVarAnnotation)
        # elif issubclass(item, Annotation):
        #     super(AnnotationDefaultDict, self).__setitem__(key, item)
        # else:
        #     _ArbitraryAnnotation = self._known_annotations[KnownAnnotations.ArbitraryAnnotation]
        #     super(AnnotationDefaultDict, self).__setitem__(key, _ArbitraryAnnotation)


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
