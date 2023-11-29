from typing import Optional, Any

from monakeeda.base import annotation_mapper, GenericAnnotation, ExceptionsDict
from monakeeda.consts import NamespacesConsts, FieldConsts
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..value_providers import ValueFieldParameter


@annotation_mapper(Optional)
class OptionalAnnotation(GenericAnnotation):
    __prior_handler__ = ValueFieldParameter

    @classmethod
    @property
    def label(cls) -> str:
        return "existence_manager"

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        if self._field_key in values:
            for component in self.managing:
                model_instance.__run_organized_components__[component] = True

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        super()._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)

        for component in self.direct_annotations:
            component.scope = f"{component.scope}.{self.__class__.__name__}"
            self.managing.append(component)

        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.REQUIRED] = False

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_optional_annotation(self, context)
