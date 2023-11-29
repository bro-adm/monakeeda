from typing import List, Type

from monakeeda.base import BaseMonkey


class GivenModelsDoNotHaveADiscriminator(Exception):
    def __init__(self, models: List[Type[BaseMonkey]]):
        self.models = models

    def __str__(self):
        return f"Discriminator provided with models that do not set a Literal for discrimination purposes -> {self.models}"


class GivenModelsHaveMoreThanOneDiscriminationKey(Exception):
    def __init__(self, models: List[Type[BaseMonkey]], keys: List[str]):
        self.models = models
        self.keys = keys

    def __str__(self):
        return f"Discriminator provided with models that have more then one discrimination key -> {list(zip(self.models, self.keys))}"


class DiscriminatorKeyNotProvidedInValues(Exception):
    def __init__(self, key: str):
        self.key = key

    def __str__(self):
        return f"{self.key} was not provided for discrimination purposes"
