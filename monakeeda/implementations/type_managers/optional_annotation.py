from typing import Optional, Any

from monakeeda.base import annotation_mapper, ExceptionsDict, Annotation, handle_manager_collisions
from monakeeda.consts import NamespacesConsts, FieldConsts
from .base_type_manager_annotation import BaseTypeManagerAnnotation
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor


@annotation_mapper(Optional)
class OptionalAnnotation(BaseTypeManagerAnnotation):
    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        relevant_components = []

        for component in self.represented_annotations:
            if self.__manage_all_sub_annotations__ or type(component) in self.__managed_components__:
                relevant_components.append(component)

        if self == monkey_cls.struct[NamespacesConsts.ANNOTATIONS][self.scope].main_annotation:
            monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.REQUIRED] = False

            for managed_component_type in self.__managed_components__:
                components = [component for component in monkey_cls.__label_organized_components__[managed_component_type.label] if type(component) == managed_component_type]

                for component in components:
                    if not isinstance(component, Annotation) and component.scope == self.scope:
                        relevant_components.append(component)

        for component in relevant_components:
            if self.label != component.label or not self.is_collision(component):
                handle_manager_collisions(self, component, decorator=self.decorator, collision_by_type=True)

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        if values.get(self._field_key, None):
            for component in self.managing:
                component.actuators.add(self)
                model_instance.__run_organized_components__[component] = True

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_optional_annotation(self, context)
