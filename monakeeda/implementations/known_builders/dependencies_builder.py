from typing import List, Any

from monakeeda.base import MonkeyBuilder, ExceptionsDict, Component
from monakeeda.consts import NamespacesConsts


class DependenciesKeysNotFieldsException(Exception):
    def __init__(self, component: Component, provided_not_strs: List[Any]):
        self.component_representor = component.representor
        self.provided_not_strs = provided_not_strs

    def __str__(self):
        return f"{self.component_representor} component was provided with not field keys dependencies -> value {self.provided_not_strs}"


class DependenciesBuilder(MonkeyBuilder):

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder: Component):
        if not main_builder.dependencies:
            pass
        elif main_builder.dependencies[0] == "*":
            main_builder.dependencies = list(monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS].keys()).copy()
            main_builder.dependencies.remove(main_builder.scope)
        else:
            not_strs = []
            for key in main_builder.dependencies:
                if not isinstance(key, str):
                    not_strs.append(key)

            if not_strs:
                exceptions[main_builder.scope].append(ValueError(f"provided from keys not all str keys -> {not_strs}"))
