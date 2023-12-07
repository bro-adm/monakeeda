from abc import ABC
from functools import lru_cache
from typing import List, Union, Tuple

from typing_extensions import get_args

from monakeeda.utils import wrap_in_list
from ..component import Component, handle_manager_collisions
from ..exceptions_manager import ExceptionsDict


class Annotation(Component, ABC):
    """
    This is the base Annotation and represents the way Monakeeda will communicate and read user set annotations.
    The responsibility of setting and initializing these annotations in set in the AnnotationManager.

    As expected it is a basic ABC implementation of the core Component object.
    As it is a per field attr, it has the _field_key attr.
    Additionally because it is a mirror of any python type, typing type, generic type or just any object it keeps the original annotation in the base_type attr
    """

    def __init__(self, field_key, set_annotation, annotations_mapping):
        super().__init__()
        self._field_key = field_key
        self._annotations_mapping = annotations_mapping
        self.set_annotation = set_annotation
        self.wrapped_by_annotations = []

    @property
    def scope(self) -> str:
        return self._field_key

    def is_collision(self, other) -> bool:
        if super().is_collision(other):

            if isinstance(other, Annotation) and self.managers is True and other.managers is True:
                return False

            return True

        return False

    @property
    def representor(self) -> str:
        return self.__class__.__name__

    @property
    def represented_types(self):
        return self.set_annotation

    @property
    def main_annotation(self):
        return self

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        relevant_components = []
        for managed_component_type in self.__managed_components__:
            components = [component for component in monkey_cls.__label_organized_components__[managed_component_type.label] if type(component) == managed_component_type]

            for component in components:
                if not isinstance(component, Annotation) and component.scope == self.scope:
                    relevant_components.append(component)

        for component in self.wrapped_by_annotations:
            if type(component) in self.__managed_components__:
                relevant_components.append(component)

        for component in relevant_components:
            if self.label != component.label or not self.is_collision(component):
                handle_manager_collisions(self, component, decorator=self.decorator, collision_by_type=True)


class GenericAnnotation(Annotation, ABC):
    """
    The base Annotation does support generics, this is only a Helper cls to allow easier APIs into getting your generics and understanding the attrs

    As what was explained above, the base_type attr holds the original user set annotation, which in this case would be:
        - List[TSomething], ...
        - Const[TSomething] / any other GenericAnnotation implementation (would inherit from Generic)

    Both these objects are either _GenericAlias or _AnnotatedAlias via the logic of how python works with Generics.
    Therefore works with get_args typing helper
    """

    __manage_all_sub_annotations__ = False

    @property
    def args(self):
        return get_args(self.set_annotation)

    @property
    @lru_cache()
    def direct_annotations(self) -> List[Annotation]:
        annotations = []

        for t in self.args:
            if t != type(None):
                self._annotations_mapping[t]
                sub_annotation = self._annotations_mapping[t](self._field_key, t, self._annotations_mapping)
                sub_annotation.wrapped_by_annotations.extend([self, *self.wrapped_by_annotations])
                annotations.append(sub_annotation)

        return annotations

    @property
    @lru_cache()
    def represented_annotations(self) -> List[Annotation]:
        """
        Returns the Monakeeda Annotations of each of the generics set in the GenericAnnotation.

        Used to usually run them as next handlers in handle_values
        """

        annotations = []

        for annotation in self.direct_annotations:
            annotations.append(annotation)
            if isinstance(annotation, GenericAnnotation):
                annotations.extend(annotation.represented_annotations)

        return annotations

    @property
    def represented_types(self) -> Union[Tuple[type], type]:
        types = []

        for annotation in self.direct_annotations:
            types.extend(wrap_in_list(annotation.represented_types))

        return tuple(types) if len(types) > 1 else types[0]

    @property
    def main_annotation(self):
        return self  # default implementation

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        super()._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)

        for component in self.represented_annotations:
            if self.__manage_all_sub_annotations__ or type(component) in self.__managed_components__:
                if self.label != component.label or not self.is_collision(component):
                    handle_manager_collisions(self, component, decorator=self.decorator, collision_by_type=True)

    def __getitem__(self, item):
        return item
