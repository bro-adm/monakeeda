from typing import Literal, Any, get_args, List

from monakeeda.base import annotation_mapper, Annotation
from monakeeda.consts import NamespacesConsts, FieldConsts
from ..optional import OptionalAnnotation
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor


@annotation_mapper(Literal)
class LiteralAnnotation(Annotation):
    __prior_handler__ = OptionalAnnotation
    # TODO: add validation that input is a single string

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: List[Exception], main_builder):
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.REQUIRED] = False
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.PRIVATE] = True
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.DISCRIMINATOR] = (self._field_key, get_args(self.base_type)[0])

        super()._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)

    def _handle_values(self, model_instance, values, stage):
        pass

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_list_annotation(self, context)