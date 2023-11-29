from typing import Literal, Any, get_args

from monakeeda.base import annotation_mapper, Annotation, ExceptionsDict
from monakeeda.consts import NamespacesConsts, FieldConsts
from .consts import DISCRIMINATION_KEY, DISCRIMINATION_VALUES, DISCRIMINATOR_NAMESPACE
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..existence_managers import OptionalAnnotation


@annotation_mapper(Literal)
class LiteralAnnotation(Annotation):
    __prior_handler__ = OptionalAnnotation

    @classmethod
    @property
    def label(cls) -> str:
        return "discrimination_setup"

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        super()._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)

        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.REQUIRED] = False
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.PRIVATE] = True
        monkey_attrs[NamespacesConsts.STRUCT][DISCRIMINATOR_NAMESPACE] = {DISCRIMINATION_KEY: self._field_key, DISCRIMINATION_VALUES: get_args(self.set_annotation)}

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        pass

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_list_annotation(self, context)
