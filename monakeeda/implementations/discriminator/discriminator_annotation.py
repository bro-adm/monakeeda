import inspect
from typing import Any, Generic, TypeVarTuple, List, get_args, Type

from monakeeda.base import BaseModel, GenericAnnotation
from monakeeda.consts import NamespacesConsts
from ..creators import CreateFrom
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..missing.errors import MissingFieldValuesException
from ..known_builders import FieldAllowedAnnotationsBuilder

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
        return f"Discriminator provided with models that have more then one discrimination key -> {zip(self.models, self.keys)}"


# class DiscriminatorKeyNotProvided


class Discriminator(GenericAnnotation, Generic[*TModels]):
    __prior_handler__ = CreateFrom
    __pass_on_errors__ = [MissingFieldValuesException]
    __builders__ = [FieldAllowedAnnotationsBuilder(BaseModel)]
    __supports_infinite__ = True

    def __init__(self, field_key, base_type, annotations_mapping):
        super().__init__(field_key, base_type, annotations_mapping)
        self._core_types = None
        self._discriminator_field_key = None
        self._monkey_mappings = {}

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: List[Exception], main_builder):
        super()._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)

        unavailable_discriminator = []
        discriminators = []

        for sub_type in self._core_types:
            sub_type.struct.setdefault(NamespacesConsts.DISCRIMINATOR, inspect._empty)
            discriminator = sub_type.struct[NamespacesConsts.DISCRIMINATOR]

            if not discriminator:
                unavailable_discriminator.append(sub_type)
            else:
                field_key, value = discriminator
                discriminators.append(field_key)
                self._monkey_mappings[value] = sub_type

        if unavailable_discriminator:
            exceptions.append(GivenModelsDoNotHaveADiscriminator(unavailable_discriminator))
        if len(set(discriminators)) > 1:
            exceptions.append(GivenModelsHaveMoreThanOneDiscriminationKey(self._core_types, discriminators))

        if not exceptions:
            self._discriminator_field_key = discriminators[0]

    def _handle_values(self, model_instance, values, stage):
        value = values[self._field_key]
        discriminator_value = value[self._discriminator_field_key]  # TODO: validate received
        monkey = self._monkey_mappings[discriminator_value]

        index = self._core_types.index(monkey)
        provided_annotation = self._annotations[index]

        provided_annotation.handle_values(model_instance, values, stage)

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_list_annotation(self, context)
