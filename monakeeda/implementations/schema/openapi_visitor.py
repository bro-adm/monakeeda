from monakeeda.base import Field, Config
from ..abstract import Abstract, AbstractParameter
from ..cast import Cast
from ..const import Const, AllowMutation
from ..creators import CreateFrom
from ..extras import ExtrasParameter
from ..general_annotations import ObjectAnnotation, BasicTypeAnnotation, UnionAnnotation, ListAnnotation, DictAnnotation
from ..generators import AliasGenerator
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..valid_values import ValidValues
from ..validators import Validator
from ..value_providers import DefaultFieldParameter, DefaultFactoryFieldParameter, AliasFieldParameter


# class OpenAPIPropertySpec(BaseModel):
#     type: str = '1'
#     format: str = '1'
#     default: str = '1'
#     description: str = '1'
#     enum: List[str] = []
#     example: str = '1'
#     minimum: str = '1'
#     maximum: str = '1'
#     ref: str = Field(alias="$ref", default='1')
#
#
# class OpenAPIObjectSpec(BaseModel):
#     type: Const[str] = Field(value='object')
#     required: List[str]
#     properties: Dict[str, OpenAPIPropertySpec]


# OpenAPIObjectSpec(required=[], properties={'a': 1, 'b': OpenAPIPropertySpec()})


class OpenAPIOperatorVisitor(ImplementationsOperatorVisitor[dict]):
    __type__ = 'openapi'

    def operate_field(self, field: Field, context: dict):
        pass

    def operate_config(self, config: Config, context: dict):
        pass

    def operate_model_annotation(self, annotation: "ModelAnnotation", context: dict):
        pass

    def operate_abstract_annotation(self, annotation: Abstract, context: dict):
        pass

    def operate_abstract_field_parameter(self, field: AbstractParameter, context: dict):
        pass

    def operate_alias_field_parameter(self, parameter: AliasFieldParameter, context: dict):
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

    def operate_default_field_parameter(self, parameter: DefaultFieldParameter, context: dict):
        pass

    def operate_default_factory_field_parameter(self, parameter: DefaultFactoryFieldParameter, context: dict):
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

    def operate_list_annotation(self, annotation: ListAnnotation, context: dict):
        pass

    def operate_dict_annotation(self, annotation: DictAnnotation, context: dict):
        pass
