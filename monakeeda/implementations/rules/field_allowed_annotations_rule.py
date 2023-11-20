from typing import Union, Any

from monakeeda.base import Rule, Parameter, RuleException
from monakeeda.consts import NamespacesConsts


class FieldAnnotationNotAllowedRuleException(RuleException):
    def __init__(self, parameter: Parameter, base_annotation, allowed_annotation: type):
        self.parameter = parameter
        self.base_annotation = base_annotation
        self.allowed_annotation = allowed_annotation

    def __str__(self):
        return f"Component {self.parameter} was set on field {self.parameter._field_key} but only supports core annotation of {self.allowed_annotation}. Was provided with {self.base_annotation}"


class FieldAllowedAnnotationsRule(Rule):
    def __init__(self, allowed_base_annotation: Any):
        self.allowed_base_annotation = allowed_base_annotation

    def validate(self, component: Parameter, monkey_cls) -> Union[RuleException, None]:
        field_annotation = monkey_cls.struct[NamespacesConsts.ANNOTATIONS][component._field_key]
        annotations_mapping = field_annotation._annotations_mapping

        annotations_mapping[self.allowed_base_annotation]
        supported_annotation = annotations_mapping[self.allowed_base_annotation](field_annotation._field_key, self.allowed_base_annotation, annotations_mapping)

        result = supported_annotation.is_same(field_annotation)
        if not result:
            return FieldAnnotationNotAllowedRuleException(component, field_annotation.base_type, self.allowed_base_annotation)

        component._core_type = result
