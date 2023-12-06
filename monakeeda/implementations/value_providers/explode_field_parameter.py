from typing import Any

from monakeeda.base import Field, BaseMonkey, get_scoped_components_by_label, ExceptionsDict, FieldParameter
from monakeeda.consts import NamespacesConsts, FieldConsts
from monakeeda.utils import get_wanted_params
from .consts import KnownLabels
from .alias_field_parameter import AliasFieldParameter
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..known_builders import ParameterValueTypeValidator, CoreAnnotationsExtractor


@Field.parameter
class ExplodeFieldParameter(FieldParameter):
    __key__ = 'explode'
    __prior_handler__ = AliasFieldParameter.label
    __builders__ = [ParameterValueTypeValidator(bool), CoreAnnotationsExtractor(BaseMonkey)]

    @classmethod
    @property
    def label(cls) -> str:
        return KnownLabels.EXTERNAL_PROVIDER

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
                self._relevant_components.extend(get_scoped_components_by_label(core_type, sub_key, KnownLabels.ALIAS_PROVIDER))
                # sub_explode = get_scoped_components_by_label(core_type, sub_key, KnownLabels.EXTERNAL_PROVIDER)

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        for sub_component in self._relevant_components:
            sub_component.handle_values(model_instance, values, stage, exceptions)

        values[self.scope] = get_wanted_params(values, self._relevant_field_keys)

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_alias_field_parameter(self, context)
