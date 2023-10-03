from abc import ABC, abstractmethod
from functools import reduce
from typing import Union, List, Set

from monakeeda.consts import NamespacesConsts


class RuleException(Exception):
    def __init__(self, component_type: str):
        self.component_type = component_type


class Rule(ABC):
    @abstractmethod
    def validate(self, component: "Component", monkey_cls) -> Union[RuleException, None]:
        pass


class RulesException(RuleException):
    def __init__(self, component_type: str, exceptions: List[RuleException]):
        super().__init__(component_type)
        self.exceptions = exceptions

    def append_exception(self, exception: RuleException):
        self.exceptions.append(exception)

    def is_empty(self) -> bool:
        return len(self.exceptions) == 0

    def __str__(self):
        if self.exceptions:
            return f"{self.component_type} validations failed -> " + str(
                reduce(lambda exc1, exc2: f'{exc1}\n{exc2}', self.exceptions))

        return str(self.exceptions)

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


class NoComponentDependenciesFailedRuleException(RuleException):
    def __init__(self, component_type: str, failed_dependencies: Set[str]):
        super().__init__(component_type)
        self.failed_dependencies = failed_dependencies

    def __str__(self):
        return f"Could not run rule validations on component {self.component_type} " \
               f"because it is dependent on prior failed components {self.failed_dependencies}"


class NoComponentDependenciesFailedRule(Rule):
    def validate(self, component: "Component", monkey_cls) -> Union[RuleException, None]:
        failed_dependencies = []

        for exception in monkey_cls.__map__[NamespacesConsts.BUILD][NamespacesConsts.EXCEPTIONS].exceptions:
            if exception.component_type in component.__dependencies__:
                failed_dependencies.append(exception.component_type)

        if failed_dependencies:
            failed_dependencies = set(failed_dependencies)
            return NoComponentDependenciesFailedRuleException(str(component.__class__), failed_dependencies)