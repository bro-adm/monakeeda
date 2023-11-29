from abc import ABC
from functools import lru_cache

from typing_extensions import get_args

from ..component import Component
from ...utils import wrap_in_list


class Annotation(Component, ABC):
    """
    This is the base Annotation and represents the way Monakeeda will communicate and read user set annotations.
    The responsibility of setting and initializing these annotations in set in the AnnotationManager.

    As expected it is a basic ABC implementation of the core Component object.
    As it is a per field attr, it has the _field_key attr.
    Additionally because it is a mirror of any python type, typing type, generic type or just any object it keeps the original annotation in the base_type attr
    """

    def __init__(self, field_key, set_annotation, annotations_mapping, is_managed=False):
        super().__init__(is_managed)
        self._field_key = field_key
        self.set_annotation = set_annotation
        self._annotations_mapping = annotations_mapping

    @classmethod
    @property
    def label(cls) -> str:
        return "type_validator"  # default implementation

    @property
    def representor(self) -> str:
        return self.__class__.__name__

    @property
    def scope(self) -> str:
        return self._field_key

    @property
    def represented_types(self):
        return self.set_annotation


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
    def args(self):
        return get_args(self.set_annotation)

    @property
    @lru_cache()
    def represented_annotations(self):
        """
            Returns the Monakeeda Annotations of each of the generics set in the GenericAnnotation.

            Used to usually run them as next handlers in handle_values
            """

        annotations = []

        for t in self.args:
            if t != type(None):
                self._annotations_mapping[t]
                sub_annotation = self._annotations_mapping[t](self._field_key, t, self._annotations_mapping)

                annotations.append(sub_annotation)
                if isinstance(sub_annotation, GenericAnnotation):
                    annotations.extend(sub_annotation.represented_annotations)

        return annotations

    @property
    def represented_types(self):
        types = []

        for t in self.args:
            if t != type(None):
                self._annotations_mapping[t]
                sub_annotation: Annotation = self._annotations_mapping[t](self._field_key, t, self._annotations_mapping)
                types.extend(wrap_in_list(sub_annotation.represented_types))

        return tuple(types) if len(types) > 1 else types[0]

    def __getitem__(self, item):
        return item
