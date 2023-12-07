from typing import Union, Any

from monakeeda.base import ExceptionsDict
from monakeeda.consts import NamespacesConsts, FieldConsts
from monakeeda.utils import get_wanted_params, wrap_in_list
from .base_decorator import BaseCreatorDecorator
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..known_builders import DependenciesBuilder


class CreateFrom(BaseCreatorDecorator):
    __builders__ = [DependenciesBuilder()]

    def __init__(self, field_key: str, dependencies: Union[list, str] = '*'):
        super(CreateFrom, self).__init__(field_key)
        self.dependencies = wrap_in_list(dependencies)

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        super(CreateFrom, self)._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)

        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self.scope][FieldConsts.DEPENDENCIES].extend(
            self.dependencies)

        for key in self.dependencies:
            monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][key][FieldConsts.REQUIRED] = True
            monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][key][FieldConsts.DEPENDENTS].append(
                self.scope)

    def _extract_relevant_exceptions(self, exceptions: ExceptionsDict):
        relevant_exceptions = super()._extract_relevant_exceptions(exceptions).copy()
        for key in self.dependencies:
            relevant_exceptions.extend(exceptions[key])

        return relevant_exceptions

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        fields_info = getattr(model_instance, NamespacesConsts.STRUCT)[NamespacesConsts.FIELDS]
        configs = getattr(model_instance, NamespacesConsts.STRUCT)[NamespacesConsts.CONFIGS]

        wanted_val = self.func(model_instance, configs, get_wanted_params(fields_info, self.dependencies),
                               get_wanted_params(values, self.dependencies))

        values[self._field_key] = wanted_val

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_create_from_decorator(self, context)
