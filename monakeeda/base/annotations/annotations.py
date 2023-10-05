from abc import ABC
from typing import Any

from .base_annotations import Annotation
from ..operator import OperatorVisitor


class BasicAnnotation(Annotation, ABC):
    def _act_with_value(self, value, cls, current_field_info, stage):
        if not isinstance(value, self.base_type):
            raise TypeError(f'{value} needs to be of type {self.base_type}')
        return value


class ModelAnnotation(BasicAnnotation):
    """
    When specifying a field type to another MonkeyModel

    class Lol(MonkeyModel):
        a: str

    class Stuz(MonkeyModel):
        lol: Lol

    The type of lol (Lol) is wrapped under the ModelAnnotation implementation
    """

    def _act_with_value(self, value, cls, current_field_info, stage):
        if isinstance(value, dict):
            return self.base_type(**value)
        else:
            return super(ModelAnnotation, self)._act_with_value(value, cls, current_field_info, stage)

    def accept_operator(self, operator_visitor: OperatorVisitor, context: Any):
        operator_visitor.operate_model_annotation(self, context)
