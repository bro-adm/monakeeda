import inspect
from typing import Union, List, Any, Dict

from monakeeda.base import Annotation, annotation_mapper, GenericAnnotation, type_validation
from .implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from .cast import Cast


@annotation_mapper(object, Any)
class ObjectAnnotation(Annotation):
    __label__ = 'object'
    __prior_handler__ = Cast

    def handle_values(self, model_instance, values, stage) -> Union[Exception, None]:
        return

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_object_annotation(self, context)


@annotation_mapper(int, str, list, dict)
class BasicTypeAnnotation(Annotation):
    __label__ = 'basic'
    __prior_handler__ = ObjectAnnotation

    def handle_values(self, model_instance, values, stage) -> Union[Exception, None]:
        return type_validation(values[self._field_key], self.base_type)

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_basic_annotation(self, context)


@annotation_mapper(Union)
class UnionAnnotation(GenericAnnotation):
    __label__ = 'union'
    __prior_handler__ = BasicTypeAnnotation

    def handle_values(self, model_instance, values, stage) -> Union[Exception, None]:
        union_types = self._types
        return type_validation(values[self._field_key], union_types)

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_union_annotation(self, context)


@annotation_mapper(List)
class ListAnnotation(GenericAnnotation):
    __label__ = 'list'
    __prior_handler__ = UnionAnnotation

    def handle_values(self, model_instance, values, stage) -> Union[Exception, None]:
        value = values[self._field_key]

        list_type = self._types
        unmatched_values = []

        for val in value:
            if not isinstance(val, list_type):
                unmatched_values.append(value)

        if unmatched_values:
            return TypeError(f'the following values are not of type {list_type} -> {unmatched_values}')

        return

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_list_annotation(self, context)


@annotation_mapper(Dict)
class DictAnnotation(GenericAnnotation):
    __label__ = 'dict'
    __prior_handler__ = ListAnnotation

    def handle_values(self, model_instance, values, stage) -> Union[Exception, None]:
        value = values[self._field_key]

        key_type, value_type = self._types
        unmatched_pairs = {}

        for key, val in value.items():
            if not isinstance(key, key_type) or not isinstance(val, value_type):
                unmatched_pairs[key] = val
                raise TypeError(f'{value} is not a dict of {key_type} key and {value_type} value -> {key}, {val}')

        if unmatched_pairs:
            return TypeError(f'{self._field_key} is not a dict of {key_type} key and {value_type} value -> {unmatched_pairs}')

        return

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_dict_annotation(self, context)
