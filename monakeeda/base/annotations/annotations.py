import inspect
from typing import Any, get_args

from .base_annotations import Annotation
from .helpers import type_validation
from ..operator import OperatorVisitor
from monakeeda.consts import NamespacesConsts


class ModelAnnotation(Annotation):
    """
    When specifying a field type to another MonkeyModel

    class Lol(MonkeyModel):
        a: str

    class Stuz(MonkeyModel):
        lol: Lol

    The type of lol (Lol) is wrapped under the ModelAnnotation implementation
    """

    __label__ = 'model'

    def _handle_values(self, model_instance, values, stage):
        value = values.get(self._field_key, inspect._empty)

        if value == inspect._empty:
            return

        elif isinstance(value, dict):
            try:
                monkey = self.base_type()
                monkey.set(**value)
            except Exception as e:
                getattr(model_instance, NamespacesConsts.EXCEPTIONS).append(e)

            values[self._field_key] = monkey

        else:
            result = type_validation(value, self.base_type)

            if result:
                getattr(model_instance, NamespacesConsts.EXCEPTIONS).append(result)

    def accept_operator(self, operator_visitor: OperatorVisitor, context: Any):
        operator_visitor.operate_model_annotation(self, context)


class TypeVarAnnotation(Annotation):

    __label__ = 'type vars'

    def _get_actual_type(self, model_instance):
        return get_args(model_instance.__orig_class__)[0]

    def _handle_values(self, model_instance, values, stage):
        from .mapping import annotation_mapping

        instance_type = self._get_actual_type(model_instance)
        annotation = annotation_mapping[instance_type](self._field_key, instance_type)

        annotation.handle_values(model_instance, values, stage)

    def accept_operator(self, operator_visitor: OperatorVisitor, context: Any):
        operator_visitor.operate_model_annotation(self, context)
