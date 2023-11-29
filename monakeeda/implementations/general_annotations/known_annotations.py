from typing import Any, get_args, TypeVar

from monakeeda.base import Annotation, type_validation, Stages, OperatorVisitor, known_annotation_mapper, \
    KnownAnnotations, BaseMonkey, ExceptionsDict
from monakeeda.consts import NamespacesConsts, TmpConsts
from .basic_annotations import BasicTypeAnnotation


@known_annotation_mapper(KnownAnnotations.TypeVarAnnotation, TypeVar, isinstance)
class TypeVarAnnotation(Annotation):
    __prior_handler__ = BasicTypeAnnotation

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

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        instance_type = self._get_actual_type(model_instance, stage)
        annotation = self._annotations_mapping[instance_type](self.scope, instance_type, self._annotations_mapping)

        annotation.handle_values(model_instance, values, stage, exceptions)

    def accept_operator(self, operator_visitor: OperatorVisitor, context: Any):
        operator_visitor.operate_model_annotation(self, context)


@known_annotation_mapper(KnownAnnotations.ModelAnnotation, BaseMonkey, issubclass)
class ModelAnnotation(Annotation):
    __prior_handler__ = TypeVarAnnotation

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        value = values[self.scope]

        if isinstance(value, dict):
            try:
                monkey = self.base_type(**value)
                values[self.scope] = monkey
            except Exception as e:
                exceptions[self.scope].append(e)

        else:
            result = type_validation(value, self.base_type)

            if result:
                exceptions[self.scope].append(result)

    def accept_operator(self, operator_visitor: OperatorVisitor, context: Any):
        operator_visitor.operate_model_annotation(self, context)


@known_annotation_mapper(KnownAnnotations.ArbitraryAnnotation, object, issubclass)
class ArbitraryAnnotation(Annotation):
    __prior_handler__ = ModelAnnotation

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        result = type_validation(values[self.scope], self.base_type)

        if result:
            exceptions[self.scope].append(result)

    def accept_operator(self, operator_visitor: OperatorVisitor, context: Any):
        operator_visitor.operate_model_annotation(self, context)
