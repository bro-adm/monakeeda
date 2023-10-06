from abc import ABC, abstractmethod
from typing import Generic

from monakeeda.base import OperatorVisitor, TOperatorContext


class ImplementationsOperatorVisitor(OperatorVisitor[TOperatorContext], ABC, Generic[TOperatorContext]):
    @abstractmethod
    def operate_abstract_annotation(self, annotation: 'Abstract', context: TOperatorContext):
        pass

    @abstractmethod
    def operate_abstract_field_parameter(self, field: 'AbstractParameter', context: TOperatorContext):
        pass

    @abstractmethod
    def operate_alias_generator_config_parameter(self, parameter: 'AliasGenerator', context: TOperatorContext):
        pass

    @abstractmethod
    def operate_alias_field_parameter(self, parameter: 'Alias', context: TOperatorContext):
        pass

    @abstractmethod
    def operate_cast_annotation(self, annotation: 'Cast', context: TOperatorContext):
        pass

    @abstractmethod
    def operate_const_annotation(self, annotation: 'Const', context: TOperatorContext):
        pass

    @abstractmethod
    def operate_const_field_parameter(self, parameter: 'AllowMutation', context: TOperatorContext):
        pass

    @abstractmethod
    def operate_create_from_decorator(self, decorator: 'CreateFrom', context: TOperatorContext):
        pass

    @abstractmethod
    def operate_default_field_parameter(self, parameter: 'DefaultParameter', context: TOperatorContext):
        pass

    @abstractmethod
    def operate_default_factory_field_parameter(self, parameter: 'DefaultFactory', context: TOperatorContext):
        pass

    @abstractmethod
    def operate_extras_config_parameter(self, parameter: 'ExtrasParameter', context: TOperatorContext):
        pass

    @abstractmethod
    def operate_valid_values_field_parameter(self, parameter: 'ValidValues', context: TOperatorContext):
        pass

    @abstractmethod
    def operate_validator_decorator(self, decorator: 'Validator', context: TOperatorContext):
        pass

    @abstractmethod
    def operate_object_annotation(self, annotation: 'ObjectAnnotation', context: TOperatorContext):
        pass

    @abstractmethod
    def operate_basic_annotation(self, annotation: 'BasicTypeAnnotation', context: TOperatorContext):
        pass

    @abstractmethod
    def operate_union_annotation(self, annotation: 'UnionAnnotation', context: TOperatorContext):
        pass

    @abstractmethod
    def operate_list_annotation(self, annotation: 'TypeListAnnotation', context: TOperatorContext):
        pass

    @abstractmethod
    def operate_no_input_field_parameter(self, parameter: 'NoInputFieldParameter', context: TOperatorContext):
        pass
