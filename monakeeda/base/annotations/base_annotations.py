from abc import ABC

from typing_extensions import get_args

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

    def __init__(self, field_key, base_type):
        self._field_key = field_key
        self.base_type = base_type

    def build(self, monkey_cls, bases, monkey_attrs):
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.ANNOTATION] = self
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.COMPONENTS].append(self)


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

    def __getitem__(self, item):
        return item
