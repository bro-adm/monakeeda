from typing import Any, Generic, TypeVarTuple, List, Type

from monakeeda.base import BaseModel, GenericAnnotation, get_parameter_component_by_identifier, ParameterIdentifier, \
    ExceptionsDict
from monakeeda.consts import NamespacesConsts, FieldConsts
from ..creators import CreateFrom
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..known_builders import CoreAnnotationsExtractor
from ..missing.errors import MissingFieldValuesException
from ...utils import get_wanted_params

TModels = TypeVarTuple("TModels")


class GivenModelsDoNotHaveADiscriminator(Exception):
    def __init__(self, models: List[Type[BaseModel]]):
        self.models = models

    def __str__(self):
        return f"Discriminator provided with models that do not set a Literal for discrimination purposes -> {self.models}"


class GivenModelsHaveMoreThanOneDiscriminationKey(Exception):
    def __init__(self, models: List[Type[BaseModel]], keys: List[str]):
        self.models = models
        self.keys = keys

    def __str__(self):
        return f"Discriminator provided with models that have more then one discrimination key -> {list(zip(self.models, self.keys))}"


class DiscriminatorKeyNotProvidedInValues(Exception):
    def __init__(self, key: str):
        self.key = key

    def __str__(self):
        return f"{self.key} was not provided for discrimination purposes"


class Discriminator(GenericAnnotation, Generic[*TModels]):
    __prior_handler__ = CreateFrom
    __pass_on_errors__ = [MissingFieldValuesException]
    __builders__ = [CoreAnnotationsExtractor(BaseModel)]
    __supports_infinite__ = True

    def __init__(self, field_key, base_type, annotations_mapping):
        super().__init__(field_key, base_type, annotations_mapping)
        self._core_types = None
        self._relevant_components = []
        self._discriminator_field_key = None
        self._monkey_mappings = {}

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        super()._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)

        unavailable_discriminator = []
        discriminators_keys = []

        for sub_type in self._core_types:
            sub_type.struct.setdefault(NamespacesConsts.DISCRIMINATOR, None)
            discriminator_info = sub_type.struct[NamespacesConsts.DISCRIMINATOR]

            if not discriminator_info:
                unavailable_discriminator.append(sub_type)
            else:
                field_key, values = discriminator_info.values()
                discriminators_keys.append(field_key)
                self._monkey_mappings.update({value: sub_type for value in values})

                sub_field = sub_type.struct[NamespacesConsts.FIELDS][field_key][FieldConsts.FIELD]
                alias_parameter = get_parameter_component_by_identifier(sub_field, 'alias', ParameterIdentifier.key)

                if alias_parameter:
                    self._relevant_components.append(alias_parameter)

        if unavailable_discriminator:
            exceptions[self._field_key].append(GivenModelsDoNotHaveADiscriminator(unavailable_discriminator))
        if len(set(discriminators_keys)) > 1:
            exceptions[self._field_key].append(GivenModelsHaveMoreThanOneDiscriminationKey(self._core_types, discriminators_keys))

        if not exceptions:
            self._discriminator_field_key = discriminators_keys[0]

    def _handle_values(self, model_instance, values, stage):
        value = values[self._field_key]
        for sub_component in self._relevant_components:
            sub_component.handle_values(model_instance, value, stage)

        relevant_values = get_wanted_params(value, [self._discriminator_field_key])
        if not relevant_values:
            getattr(model_instance, NamespacesConsts.EXCEPTIONS).append(DiscriminatorKeyNotProvidedInValues(self._discriminator_field_key))

        else:
            discriminator_value = value[self._discriminator_field_key]
            monkey = self._monkey_mappings[discriminator_value]

            index = self._core_types.index(monkey)
            provided_annotation = self._annotations[index]
            provided_annotation.handle_values(model_instance, values, stage)

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_list_annotation(self, context)
