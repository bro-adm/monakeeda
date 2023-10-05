from monakeeda.base import Field, Config, ModelAnnotation
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..abstract import Abstract, AbstractParameter
from ..alias import Alias, AliasGenerator
from ..cast import Cast
from ..const import Const, AllowMutation
from ..creators import CreateFrom
from ..default import DefaultParameter, DefaultFactory
from ..extras import ExtrasParameter
from ..valid_values import ValidValues
from ..validators import Validator
from ..basic_annotations import ObjectAnnotation, BasicTypeAnnotation, UnionAnnotation, TypeListAnnotation


class SchemaOperatorVisitor(ImplementationsOperatorVisitor[dict]):
    __type__ = 'schema'

    def operate_field(self, field: Field, context: dict):
        pass

    def operate_config(self, config: Config, context: dict):
        pass

    def operate_model_annotation(self, annotation: ModelAnnotation, context: dict):
        pass

    def operate_abstract_annotation(self, annotation: Abstract, context: dict):
        pass

    def operate_abstract_field_parameter(self, field: AbstractParameter, context: dict):
        pass

    def operate_alias_field_parameter(self, parameter: Alias, context: dict):
        pass

    def operate_alias_generator_config_parameter(self, parameter: AliasGenerator, context: dict):
        pass

    def operate_cast_annotation(self, annotation: Cast, context: dict):
        pass

    def operate_const_annotation(self, annotation: Const, context: dict):
        pass

    def operate_const_field_parameter(self, parameter: AllowMutation, context: dict):
        pass

    def operate_create_from_decorator(self, decorator: CreateFrom, context: dict):
        pass

    def operate_default_field_parameter(self, parameter: DefaultParameter, context: dict):
        pass

    def operate_default_factory_field_parameter(self, parameter: DefaultFactory, context: dict):
        pass

    def operate_extras_config_parameter(self, parameter: ExtrasParameter, context: dict):
        pass

    def operate_valid_values_field_parameter(self, parameter: ValidValues, context: dict):
        pass

    def operate_validator_decorator(self, decorator: Validator, context: dict):
        pass

    def operate_object_annotation(self, annotation: ObjectAnnotation, context: dict):
        pass

    def operate_basic_annotation(self, annotation: BasicTypeAnnotation, context: dict):
        pass

    def operate_union_annotation(self, annotation: UnionAnnotation, context: dict):
        pass

    def operate_list_annotation(self, annotation: TypeListAnnotation, context: dict):
        pass
