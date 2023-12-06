from typing import Any

from monakeeda.base import Field, Stages, ExceptionsDict, FieldParameter, ScopedLabeledComponentsCollisionsException
from monakeeda.consts import NamespacesConsts, FieldConsts
from monakeeda.utils import get_wanted_params
from .consts import KnownLabels
from .default_factory_field_parameter import DefaultFactoryFieldParameter
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor


@Field.parameter
class ValueFieldParameter(FieldParameter):
    __key__ = 'value'
    __prior_handler__ = DefaultFactoryFieldParameter.label

    @classmethod
    @property
    def label(cls) -> str:
        return KnownLabels.MAIN_PROVIDER

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        super()._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.REQUIRED] = False

        scoped_collisions = get_wanted_params(monkey_cls.scopes[self.scope], [KnownLabels.DEFAULT_PROVIDER, KnownLabels.EXTERNAL_PROVIDER])
        if scoped_collisions:
            collision_components = set[str]()
            for label, components in scoped_collisions.items():
                collision_components.update({component.representor for component in components})

            exceptions[self.scope].append(ScopedLabeledComponentsCollisionsException(self.label, collision_components, self.representor))

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        if stage == Stages.INIT:
            values[self._field_key] = self.param_val

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_default_field_parameter(self, context)
