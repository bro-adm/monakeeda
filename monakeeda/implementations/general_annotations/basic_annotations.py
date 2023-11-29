from typing import Union, List, Any, Dict

from monakeeda.base import Annotation, annotation_mapper, GenericAnnotation, type_validation, ExceptionsDict
from ..existence_managers import CreateFrom
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor


@annotation_mapper(object, Any)
class ObjectAnnotation(Annotation):
    __prior_handler__ = CreateFrom

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        pass

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_object_annotation(self, context)


@annotation_mapper(int, str, list, dict)
class BasicTypeAnnotation(Annotation):
    __prior_handler__ = ObjectAnnotation

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        result = type_validation(values[self.scope], self.base_type)

        if result:
            exceptions[self.scope].append(result)

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_basic_annotation(self, context)


@annotation_mapper(Union)
class UnionAnnotation(GenericAnnotation):
    __prior_handler__ = BasicTypeAnnotation

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        union_types = self._types

        result = type_validation(values[self.scope], union_types)

        if result:
            exceptions[self.scope].append(result)

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_union_annotation(self, context)


@annotation_mapper(List)
class ListAnnotation(GenericAnnotation):
    __prior_handler__ = UnionAnnotation

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        value = values[self.scope]

        list_type = self._types
        unmatched_values = []

        for val in value:
            if not isinstance(val, list_type):
                unmatched_values.append(value)

        if unmatched_values:
            exceptions[self.scope].append(
                TypeError(f'the following values are not of type {list_type} -> {unmatched_values}'))

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_list_annotation(self, context)


@annotation_mapper(Dict)
class DictAnnotation(GenericAnnotation):
    __prior_handler__ = ListAnnotation

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        value = values[self.scope]

        key_type, value_type = self._types
        unmatched_pairs = {}

        for key, val in value.items():
            if not isinstance(key, key_type) or not isinstance(val, value_type):
                unmatched_pairs[key] = val

        if unmatched_pairs:
            exceptions[self.scope].append(TypeError(
                f'{self._field_key} is not a dict of {key_type} key and {value_type} value -> {unmatched_pairs}'))

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_dict_annotation(self, context)
