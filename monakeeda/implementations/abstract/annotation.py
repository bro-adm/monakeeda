from typing import Generic, T, Any

from monakeeda.base import GenericAnnotation, Config, ExceptionsDict
from .consts import ABSTRACT_MANAGER
from .exceptions import AbstractFieldFoundError
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor


class Abstract(GenericAnnotation, Generic[T]):
    __prior_handler__ = Config

    @classmethod
    @property
    def label(cls) -> str:
        return ABSTRACT_MANAGER

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        exceptions[self.scope].append(AbstractFieldFoundError())

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_abstract_annotation(self, context)
