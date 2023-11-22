from typing import Literal, Any, get_args, List

from monakeeda.base import annotation_mapper, Annotation
from monakeeda.consts import NamespacesConsts, FieldConsts, DiscriminationConsts
from ..optional import OptionalAnnotation
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor


@annotation_mapper(Literal)
class LiteralAnnotation(Annotation):
    __prior_handler__ = OptionalAnnotation

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: List[Exception], main_builder):
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.REQUIRED] = False
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.PRIVATE] = True
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.DISCRIMINATOR] = {DiscriminationConsts.FIELD_KEY: self._field_key, DiscriminationConsts.VALUES: get_args(self.base_type)}

        super()._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)

    def _handle_values(self, model_instance, values, stage):
        pass

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_list_annotation(self, context)
