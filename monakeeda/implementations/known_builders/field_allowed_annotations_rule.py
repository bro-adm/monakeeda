from typing import Any, List, get_origin, get_args

from monakeeda.base import Parameter, MonkeyBuilder, Annotation
from monakeeda.consts import NamespacesConsts


class FieldAnnotationNotAllowedException(Exception):
    def __init__(self, parameter: Parameter, base_annotation, allowed_annotation: type):
        self.parameter = parameter
        self.base_annotation = base_annotation
        self.allowed_annotation = allowed_annotation

    def __str__(self):
        return f"Component {self.parameter} was set on field {self.parameter._field_key} but only supports core annotation of {self.allowed_annotation}. Was provided with {self.base_annotation}"


class FieldAllowedAnnotationsBuilder(MonkeyBuilder):
    def __init__(self, allowed_base_annotation: Any):
        self.allowed_base_annotation = allowed_base_annotation

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: List[Exception], main_builder):
        field_annotation = monkey_cls.struct[NamespacesConsts.ANNOTATIONS][main_builder._field_key]
        annotations_mapping = field_annotation._annotations_mapping

        if isinstance(main_builder, Annotation):
            main_builder_origin = get_origin(main_builder.base_type)
            self.allowed_base_annotation = main_builder_origin[self.allowed_base_annotation]

        annotations_mapping[self.allowed_base_annotation]
        supported_annotation = annotations_mapping[self.allowed_base_annotation](field_annotation._field_key, self.allowed_base_annotation, annotations_mapping)

        result = supported_annotation.is_same(field_annotation)
        if not result:
            exceptions.append(FieldAnnotationNotAllowedException(main_builder, field_annotation.base_type, self.allowed_base_annotation))

        if isinstance(main_builder, Annotation):
            main_builder._core_types = get_args(result)
        else:
            main_builder._core_types = result
