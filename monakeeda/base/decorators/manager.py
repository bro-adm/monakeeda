from functools import reduce
from typing import List

from monakeeda.consts import NamespacesConsts, DecoratorConsts
from .base_decorator import BaseDecorator
from ..exceptions_manager import ExceptionsDict
from ..meta import ComponentManager


class DecoratorManager(ComponentManager):
    """
    The Decorator Manager does not need to be aware of the Decorator types because it does not have the responsability to initialzie them.
    This manager only needs to find them and make sure that collisions are removed.

    Finding the decorators happens via the known namespace set on each Monakeeda decorated method.
    All Decorators use the same namespace, so this Manager does not need to acknowledge any specific type.

    These overall concepts are the reason that decorators unlike other components do not have the overridability logic like Fields, Annotations and Configs.
    """

    def _components(self, monkey_cls) -> List[BaseDecorator]:
        decorators_info = getattr(monkey_cls, NamespacesConsts.STRUCT)[NamespacesConsts.DECORATORS]

        return reduce(lambda x1, x2: [*x1, *x2], decorators_info.values(), [])

    def _set_by_base(self, monkey_cls, base, attrs, collisions):
        current_decorators_info = attrs[NamespacesConsts.STRUCT][NamespacesConsts.DECORATORS]  # prior bases merged set of fields
        base_decorators_info = base.struct[NamespacesConsts.DECORATORS]  # current base set of fields

        current_decorators_funcs = set(current_decorators_info.keys())
        base_decorators_funcs = set(base_decorators_info.keys())

        collided_funcs = current_decorators_funcs & base_decorators_funcs  # intersection

        for func_name in collided_funcs:
            attrs.pop(func_name)

        new_decorated_funcs = base_decorators_funcs - current_decorators_funcs
        for new_decorated_func in new_decorated_funcs:
            if new_decorated_func not in collided_funcs:
                new_decorators = base.struct[NamespacesConsts.DECORATORS][new_decorated_func]
                monkey_cls.struct[NamespacesConsts.DECORATORS][new_decorated_func] = new_decorators

    def _set_curr_cls(self, monkey_cls, bases, monkey_attrs):
        for attr, attr_val in monkey_attrs.items():
            decorated_with = getattr(attr_val, DecoratorConsts.DECORATED_WITH, None)
            if decorated_with:
                # attr_val in here is a decorated method
                monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.DECORATORS][attr] = decorated_with

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        monkey_attrs[NamespacesConsts.STRUCT].setdefault(NamespacesConsts.DECORATORS, {})
        super(DecoratorManager, self)._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)
