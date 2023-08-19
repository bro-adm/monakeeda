from typing import Union, List, Any

from monakeeda.base import Annotation, annotation_mapper, GenericAnnotation


@annotation_mapper(object, Any)
class ObjectAnnotation(Annotation):
    def _act_with_value(self, value, *_, **__):
        return value


@annotation_mapper(int, str, list)
class BasicTypeAnnotation(Annotation):
    def _act_with_value(self, value, *_, **__):
        if not isinstance(value, self.base_type):
            raise TypeError(f'{value} is not a {self.base_type.__name__}')
        return value


@annotation_mapper(Union)
class UnionAnnotation(GenericAnnotation):
    def _act_with_value(self, value, *_, **__):
        union_types = self._types
        if not isinstance(value, union_types):
            raise TypeError(f'{value} is not one of possible types {union_types}')
        return value


@annotation_mapper(List)
class TypeListAnnotation(GenericAnnotation):
    def _act_with_value(self, value, *_, **__):
        list_types = self._types
        for val in value:
            if not isinstance(val, list_types):
                raise TypeError(f'{val} is not one of possible types {list_types}')
        return value
