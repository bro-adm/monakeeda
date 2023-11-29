from typing import Union, Any

from monakeeda.base import annotation_mapper, ExceptionsDict, GenericAnnotation
from .base_infinite_args_annotation import BaseInfiniteArgsAnnotation
from .consts import KnownLabels
from ..existence_managers import CreateFrom
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor


@annotation_mapper(Union)
class UnionAnnotation(BaseInfiniteArgsAnnotation):
    __prior_handler__ = CreateFrom

    @classmethod
    @property
    def label(cls) -> str:
        return KnownLabels.TYPE_MANAGER

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        value = values[self._field_key]

        types = [annotation.represented_types for annotation in self.direct_annotations]
        annotation = None

        for i in range(len(types)):
            type_group = types[i]

            if isinstance(value, type_group):
                annotation = self.direct_annotations[i]
                break

        if annotation:
            relevant_annotations = [annotation]

            if isinstance(annotation, GenericAnnotation):
                relevant_annotations.extend(annotation.represented_annotations)

            for relevant_annotation in relevant_annotations:
                model_instance.__run_organized_components__[relevant_annotation] = True

        else:
            exceptions[self.scope].append(TypeError(f'{value} needs to be of type/s {self.represented_types}'))

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_union_annotation(self, context)
