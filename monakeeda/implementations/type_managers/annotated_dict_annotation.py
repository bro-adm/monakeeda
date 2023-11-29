from typing import Dict, Any

from monakeeda.base import annotation_mapper, GenericAnnotation, ExceptionsDict
from .annotated_list_annotation import ListAnnotation
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor


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
