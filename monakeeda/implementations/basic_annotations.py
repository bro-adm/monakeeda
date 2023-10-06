from typing import Union, List, Any

from monakeeda.base import Annotation, annotation_mapper, GenericAnnotation
from .implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from .cast import Cast


@annotation_mapper(object, Any)
class ObjectAnnotation(Annotation):
    __label__ = 'object'
    __prior_handler__ = Cast

    def _act_with_value(self, value, *_, **__):
        return value

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_object_annotation(self, context)


@annotation_mapper(int, str, list)
class BasicTypeAnnotation(Annotation):
    __label__ = 'basic'
    __prior_handler__ = ObjectAnnotation

    def _act_with_value(self, value, *_, **__):
        if not isinstance(value, self.base_type):
            raise TypeError(f'{value} is not a {self.base_type.__name__}')
        return value

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_basic_annotation(self, context)


@annotation_mapper(Union)
class UnionAnnotation(GenericAnnotation):
    __label__ = 'union'
    __prior_handler__ = BasicTypeAnnotation

    def _act_with_value(self, value, *_, **__):
        union_types = self._types
        if not isinstance(value, union_types):
            raise TypeError(f'{value} is not one of possible types {union_types}')
        return value

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_union_annotation(self, context)


@annotation_mapper(List)
class TypeListAnnotation(GenericAnnotation):
    __label__ = 'list'
    __prior_handler__ = UnionAnnotation

    def _act_with_value(self, value, *_, **__):
        list_types = self._types
        for val in value:
            if not isinstance(val, list_types):
                raise TypeError(f'{val} is not one of possible types {list_types}')
        return value

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_list_annotation(self, context)
