import inspect
from typing import Any, get_args

from monakeeda.consts import NamespacesConsts, TmpConsts
from .base_annotations import Annotation
from .helpers import type_validation
from ..interfaces import Stages
from ..operator import OperatorVisitor


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
                monkey = self.base_type(**value)
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
    __prior_handler__ = ModelAnnotation
    __label__ = 'type vars'

    def _get_actual_type(self, model_instance, stage):
        model_tmp = getattr(model_instance, NamespacesConsts.TMP)

        if stage == Stages.INIT:
            instance_types = model_tmp[TmpConsts.GENERICS]  # provided generics for model - either new TypeVar or an actual type
        else:
            # stage => Stages.UPDATE
            instance_types = get_args(model_instance.__orig_class__)  # preserves order

        model_generics = model_instance.__class__.__parameters__  # saved attr for Generics -> saved in tuple which preserves order

        index = model_generics.index(self.base_type)  # in this specific anntoation the base_type is mapped to the TypeVar instance
        return instance_types[index]

    def _handle_values(self, model_instance, values, stage):
        from .mapping import annotation_mapping

        instance_type = self._get_actual_type(model_instance, stage)
        annotation = annotation_mapping[instance_type](self._field_key, instance_type)

        annotation.handle_values(model_instance, values, stage)

    def accept_operator(self, operator_visitor: OperatorVisitor, context: Any):
        operator_visitor.operate_model_annotation(self, context)


class ArbitraryAnnotation(Annotation):
    __label__ = 'basic'
    __prior_handler__ = TypeVarAnnotation
    # __pass_on_errors__ = [MissingFieldValuesException]

    def _handle_values(self, model_instance, values, stage):
        result = type_validation(values[self._field_key], self.base_type)

        if result:
            getattr(model_instance, NamespacesConsts.EXCEPTIONS).append(result)

    def accept_operator(self, operator_visitor: OperatorVisitor, context: Any):
        operator_visitor.operate_model_annotation(self, context)
