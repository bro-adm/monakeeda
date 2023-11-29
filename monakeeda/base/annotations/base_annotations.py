from abc import ABC

from typing_extensions import get_args

from ..component import Component


class Annotation(Component, ABC):
    """
    This is the base Annotation and represents the way Monakeeda will communicate and read user set annotations.
    The responsibility of setting and initializing these annotations in set in the AnnotationManager.

    As expected it is a basic ABC implementation of the core Component object.
    As it is a per field attr, it has the _field_key attr.
    Additionally because it is a mirror of any python type, typing type, generic type or just any object it keeps the original annotation in the base_type attr
    """

    def __init__(self, field_key, base_type, annotations_mapping, is_managed=False):
        super().__init__(is_managed)
        self._field_key = field_key
        self.base_type = base_type
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
    def core_types(self):
        return self.base_type


class GenericAnnotation(Annotation, ABC):
    """
    The base Annotation does support generics, this is only a Helper cls to allow easier APIs into getting your generics and understanding the attrs

    As what was explained above, the base_type attr holds the original user set annotation, which in this case would be:
        - List[TSomething], ...
        - Const[TSomething] / any other GenericAnnotation implementation (would inherit from Generic)

    Both these objects are either _GenericAlias or _AnnotatedAlias via the logic of how python works with Generics.
    Therefore works with get_args typing helper
    """
    __supports_infinite__ = False

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

    @property
    def core_types(self):
        types = []
        for annotation in self._annotations:
            types.append(annotation.core_types)

        return tuple(types) if len(types) > 1 else types[0]

    def __getitem__(self, item):
        return item
