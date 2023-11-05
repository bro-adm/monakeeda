import inspect
from typing import Generic, T, Any, Union

from monakeeda.base import GenericAnnotation, Stages, get_generics_annotations
from .exceptions import ConstError
from ..creators import CreateFrom
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from monakeeda.consts import NamespacesConsts


class Const(GenericAnnotation, Generic[T]):
    __label__ = 'const'
    __prior_handler__ = CreateFrom

    def _handle_values(self, model_instance, values, stage):
        value = values[self._field_key]

        if stage == Stages.INIT:
            get_generics_annotations(self)[0].handle_values(model_instance, values, stage)

        elif stage == Stages.UPDATE:
            curr_val = getattr(model_instance, self._field_key)

            if value != curr_val:
                getattr(model_instance, NamespacesConsts.EXCEPTIONS).append(ConstError(curr_val, value))

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_const_annotation(self, context)