from typing import Any, Generic, TypeVarTuple

from monakeeda.base import BaseMonkey, GenericAnnotation, ExceptionsDict, get_scoped_components_by_label
from .consts import DISCRIMINATOR_NAMESPACE, KnownLabels
from .exceptions import DiscriminatorKeyNotProvidedInValues, GivenModelsDoNotHaveADiscriminator, GivenModelsHaveMoreThanOneDiscriminationKey
from .union_annotation import UnionAnnotation
from ..value_providers import KnownLabels
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..known_builders import CoreAnnotationsExtractor
from ...utils import get_wanted_params

TModels = TypeVarTuple("TModels")


class Discriminator(GenericAnnotation, Generic[*TModels]):
    __prior_handler__ = UnionAnnotation
    __builders__ = [CoreAnnotationsExtractor(BaseMonkey)]
    __supports_infinite__ = True

    @classmethod
    @property
    def label(cls) -> str:
        return KnownLabels.TYPE_MANAGER

    def __init__(self, field_key, set_annotation, annotations_mapping):
        super().__init__(field_key, set_annotation, annotations_mapping)
        self._core_types = None
        self._relevant_components = []
        self._discriminator_field_key = None
        self._monkey_mappings = {}

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        super()._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)

        unavailable_discriminator = []
        discriminators_keys = []

        for sub_type in self._core_types:
            sub_type.struct.setdefault(DISCRIMINATOR_NAMESPACE, None)
            discriminator_info = sub_type.struct[DISCRIMINATOR_NAMESPACE]

            if not discriminator_info:
                unavailable_discriminator.append(sub_type)
            else:
                field_key, values = discriminator_info.values()
                discriminators_keys.append(field_key)
                self._monkey_mappings.update({value: sub_type for value in values})
                self._relevant_components.extend(get_scoped_components_by_label(sub_type, field_key, KnownLabels.ALIAS_PROVIDER))

        if unavailable_discriminator:
            exceptions[self._field_key].append(GivenModelsDoNotHaveADiscriminator(unavailable_discriminator))
        if len(set(discriminators_keys)) > 1:
            exceptions[self._field_key].append(GivenModelsHaveMoreThanOneDiscriminationKey(self._core_types, discriminators_keys))

        if not exceptions:
            self._discriminator_field_key = discriminators_keys[0]

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        value = values[self._field_key]
        for sub_component in self._relevant_components:
            sub_component.handle_values(model_instance, value, stage, exceptions)

        relevant_values = get_wanted_params(value, [self._discriminator_field_key])
        if not relevant_values:
            exceptions[self.scope].append(DiscriminatorKeyNotProvidedInValues(self._discriminator_field_key))

        else:
            discriminator_value = value[self._discriminator_field_key]
            monkey = self._monkey_mappings[discriminator_value]

            index = self._core_types.index(monkey)
            provided_annotation = self.represented_annotations[index]
            provided_annotation.handle_values(model_instance, values, stage, exceptions)

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_list_annotation(self, context)
