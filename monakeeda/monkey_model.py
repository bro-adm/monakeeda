from typing import List, Type, Union

from monakeeda.base import BaseModel, ConfigurableComponent, Rules
from monakeeda.consts import NamespacesConsts
from monakeeda.utils import is_subset
from .base import Config as BaseConfig, Rule, RuleException
from .implementations import OpenAPIOperatorVisitor, ValidateMissingFieldsConfigParameter


class RequiredParametersNotSetRuleException(RuleException):
    def __init__(self, configurable_component_type: Type[ConfigurableComponent], required_keys: List[str]):
        self.configurable_component_type = configurable_component_type
        self.required_keys = required_keys

    def __str__(self):
        return f"The following parameters were not provided for {self.configurable_component_type} -> {self.required_keys}"


class RequiredParametersAreSetRule(Rule):
    def __init__(self, required_keys: List[str]):
        self.required_keys = required_keys

    def validate(self, component: ConfigurableComponent, monkey_cls) -> Union[RuleException, None]:
        initialized_parameters_keys = [parameter.__key__ for parameter in component._parameters]

        return None if is_subset(initialized_parameters_keys, self.required_keys) else RequiredParametersNotSetRuleException(type(component), self.required_keys)


class Config(BaseConfig):
    __rules__ = Rules([*BaseConfig.__rules__._rules, RequiredParametersAreSetRule([ValidateMissingFieldsConfigParameter.__key__])])


class MonkeyModel(BaseModel):
    @classmethod
    def openapi(cls) -> dict:
        model_schema = getattr(cls, NamespacesConsts.FIELDS).copy()
        cls._operate(cls, OpenAPIOperatorVisitor.__type__, model_schema)

        return model_schema

    class Config:
        validate_missing_fields = True
