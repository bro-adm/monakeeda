from abc import ABC, abstractmethod
from functools import reduce
from typing import Union, List


class RuleException(Exception):
    pass


class Rule(ABC):
    @abstractmethod
    def validate(self, component: "Component", monkey_cls) -> Union[RuleException, None]:
        pass


class RulesException(RuleException):
    def __init__(self, component_type: str, exceptions: List[RuleException]):
        self._component_type = component_type
        self._exceptions = exceptions

    def append_exception(self, exception: RuleException):
        self._exceptions.append(exception)

    def __str__(self):
        return f"{self._component_type} validations failed -> " + str(
            reduce(lambda exc1, exc2: f'{exc1}\n{exc2}', self._exceptions))

    __repr__ = __str__


class Rules(Rule):
    def __init__(self, rules: List[Rule]):
        self._rules = rules

    def validate(self, component: "Component", monkey_cls) -> Union[RuleException, None]:
        exceptions = []
        for rule in self._rules:
            result = rule.validate(component, monkey_cls)
            if result:
                exceptions.append(result)

        if exceptions:
            return RulesException(component.__class__.__name__, exceptions)

        return
