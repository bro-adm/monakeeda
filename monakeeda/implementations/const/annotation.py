import inspect
from typing import Generic, T, Any, Union

from monakeeda.base import GenericAnnotation, Stages
from .exceptions import ConstError
from ..creators import CreateFrom
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor


class Const(GenericAnnotation, Generic[T]):
    __label__ = 'const'
    __prior_handler__ = CreateFrom

    def handle_values(self, model_instance, values, stage) -> Union[Exception, None]:
        value = values.get(self._field_key, inspect._empty)

        if value == inspect._empty:
            return

        if stage == Stages.INIT:
            const_type = self._types[0]

            if not isinstance(value, const_type):
                return TypeError(f"field should be of type {const_type}, but got {value} of type {type(value)} instead")

        elif stage == Stages.UPDATE:
            curr_val = getattr(model_instance, self._field_key)

            if value != curr_val:
                return ConstError(curr_val, value)

        return

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_const_annotation(self, context)