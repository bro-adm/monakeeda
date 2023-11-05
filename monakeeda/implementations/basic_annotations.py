import inspect
from typing import Union, List, Any, Dict

from monakeeda.base import Annotation, annotation_mapper, GenericAnnotation, type_validation
from .implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from .cast import Cast
from monakeeda.consts import NamespacesConsts
from .missing.errors import MissingFieldValuesException


@annotation_mapper(object, Any)
class ObjectAnnotation(Annotation):
    __label__ = 'object'
    __prior_handler__ = Cast
    __pass_on_errors__ = [MissingFieldValuesException]

    def _handle_values(self, model_instance, values, stage):
        pass

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_object_annotation(self, context)


@annotation_mapper(int, str, list, dict)
class BasicTypeAnnotation(Annotation):
    __label__ = 'basic'
    __prior_handler__ = ObjectAnnotation
    __pass_on_errors__ = [MissingFieldValuesException]

    def _handle_values(self, model_instance, values, stage):
        result = type_validation(values[self._field_key], self.base_type)

        if result:
            getattr(model_instance, NamespacesConsts.EXCEPTIONS).append(result)

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_basic_annotation(self, context)


@annotation_mapper(Union)
class UnionAnnotation(GenericAnnotation):
    __label__ = 'union'
    __prior_handler__ = BasicTypeAnnotation
    __pass_on_errors__ = [MissingFieldValuesException]

    def _handle_values(self, model_instance, values, stage):
        union_types = self._types

        result = type_validation(values[self._field_key], union_types)

        if result:
            getattr(model_instance, NamespacesConsts.EXCEPTIONS).append(result)

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_union_annotation(self, context)


@annotation_mapper(List)
class ListAnnotation(GenericAnnotation):
    __label__ = 'list'
    __prior_handler__ = UnionAnnotation
    __pass_on_errors__ = [MissingFieldValuesException]

    def _handle_values(self, model_instance, values, stage):
        value = values[self._field_key]

        list_type = self._types
        unmatched_values = []

        for val in value:
            if not isinstance(val, list_type):
                unmatched_values.append(value)

        if unmatched_values:
            getattr(model_instance, NamespacesConsts.EXCEPTIONS).append(TypeError(f'the following values are not of type {list_type} -> {unmatched_values}'))

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_list_annotation(self, context)


@annotation_mapper(Dict)
class DictAnnotation(GenericAnnotation):
    __label__ = 'dict'
    __prior_handler__ = ListAnnotation
    __pass_on_errors__ = [MissingFieldValuesException]

    def _handle_values(self, model_instance, values, stage):
        value = values[self._field_key]

        key_type, value_type = self._types
        unmatched_pairs = {}

        for key, val in value.items():
            if not isinstance(key, key_type) or not isinstance(val, value_type):
                unmatched_pairs[key] = val

        if unmatched_pairs:
            getattr(model_instance, NamespacesConsts.EXCEPTIONS).append(TypeError(f'{self._field_key} is not a dict of {key_type} key and {value_type} value -> {unmatched_pairs}'))

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_dict_annotation(self, context)
