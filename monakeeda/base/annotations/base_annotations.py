from abc import ABC
from typing import Any, Union

from typing_extensions import get_args, get_origin

from monakeeda.consts import NamespacesConsts, FieldConsts
from ..component import Component


class Annotation(Component, ABC):
    """
    This is the base Annotation and represents the way Monakeeda will communicate and read user set annotations.
    The responsibility of setting and initializing these annotations in set in the AnnotationManager.

    As expected it is a basic ABC implementation of the core Component object.
    As it is a per field attr, it has the _field_key attr.
    Additionally because it is a mirror of any python type, typing type, generic type or just any object it keeps the original annotation in the base_type attr
    """

    def __init__(self, field_key, base_type, annotations_mapping):
        self._field_key = field_key
        self.base_type = base_type
        self._annotations_mapping = annotations_mapping

    def build(self, monkey_cls, bases, monkey_attrs):
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.ANNOTATION] = self
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.COMPONENTS].append(self)

    def is_same(self, other) -> Union[Any, bool]:
        if isinstance(other, GenericAnnotation):
            annotations = other._annotations
            if len(annotations) > 1:
                return False

            return self.is_same(annotations[0])

        if issubclass(other.base_type, self.base_type):
            return other.base_type


class GenericAnnotation(Annotation, ABC):
    """
    The base Annotation does support generics, this is only a Helper cls to allow easier APIs into getting your generics and understanding the attrs

    As what was explained above, the base_type attr holds the original user set annotation, which in this case would be:
        - List[TSomething], ...
        - Const[TSomething] / any other GenericAnnotation implementation (would inherit from Generic)

    Both these objects are either _GenericAlias or _AnnotatedAlias via the logic of how python works with Generics.
    Therefore works with get_args typing helper
    """

    @property
    def _types(self):
        return get_args(self.base_type)

    @property
    def _annotations(self):
        """
            Returns the Monakeeda Annotations of each of the generics set in the GenericAnnotation.

            Used to usually run them as next handlers in handle_values
            """

        annotations = []

        for t in self._types:
            if t != type(None):
                self._annotations_mapping[t]
                annotations.append(self._annotations_mapping[t](self._field_key, t, self._annotations_mapping))

        return annotations

    def is_same(self, other) -> Union[Any, bool]:
        scoped_annotation = get_origin(other.base_type)
        scoped_sub_annotations = []

        annotations = self._annotations

        if isinstance(other, GenericAnnotation):
            other_annotations = other._annotations

            if len(other_annotations) == 1:
                return self.is_same(other_annotations[0])

            elif len(annotations) != len(other_annotations):
                return False

            annotations_zip = zip(annotations, other_annotations)

            for annotation, other_annotation in annotations_zip:
                result = annotation.is_same(other_annotation)
                if not result:
                    return False

                scoped_sub_annotations.append(result)

            return scoped_annotation[tuple(scoped_sub_annotations)]

        if len(annotations) == 1:  # also means that other is of type Annotation
            return annotations[0].is_same(other)

        return False

    def __getitem__(self, item):
        return item
