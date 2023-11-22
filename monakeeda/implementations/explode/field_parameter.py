from typing import Any

from monakeeda.base import FieldParameter, Field, BaseModel, get_parameter_component_by_identifier, ParameterIdentifier, \
    ExceptionsDict
from monakeeda.consts import NamespacesConsts, FieldConsts
from monakeeda.utils import get_wanted_params
from ..abstract import AbstractParameter
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..known_builders import ParameterValueTypeValidator, CoreAnnotationsExtractor


@Field.parameter
class ExplodeFieldParameter(FieldParameter):
    __key__ = 'explode'
    __label__ = 'initialization'
    __prior_handler__ = AbstractParameter
    __builders__ = [ParameterValueTypeValidator(bool), CoreAnnotationsExtractor(BaseModel)]

    def __init__(self, param_val, field_key):
        super().__init__(param_val, field_key)
        self._core_types = None
        self._relevant_components = []
        self._relevant_field_keys = []

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        super()._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.REQUIRED] = False

        for core_type in self._core_types:
            for sub_key, sub_field_info in core_type.struct[NamespacesConsts.FIELDS].items():
                self._relevant_field_keys.append(sub_key)

                sub_field = sub_field_info[FieldConsts.FIELD]
                alias_parameter = get_parameter_component_by_identifier(sub_field, 'alias', ParameterIdentifier.key)

                if alias_parameter:
                    self._relevant_components.append(alias_parameter)

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        for sub_component in self._relevant_components:
            sub_component.handle_values(model_instance, values, stage, exceptions)

        values[self._field_key] = get_wanted_params(values, self._relevant_field_keys)

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_alias_field_parameter(self, context)
