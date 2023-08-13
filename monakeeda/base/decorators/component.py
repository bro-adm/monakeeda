from typing import List

from monakeeda.consts import NamespacesConsts
from .base_decorator import BaseDecorator
from ..component import MainComponent


class DecoratorMainComponent(MainComponent[BaseDecorator]):

    def _components(self, monkey_cls) -> List[BaseDecorator]:
        return monkey_cls.__map__[NamespacesConsts.BUILD][NamespacesConsts.DECORATORS]

    # TODO: fix the issue that happens when overriden -> investigate!!!
    def _set_by_base(self, monkey_cls, base, attrs):
        monkey_cls.__map__[NamespacesConsts.BUILD][NamespacesConsts.DECORATORS].extend(
            base.__map__[NamespacesConsts.BUILD][NamespacesConsts.DECORATORS])

    # TODO: decide if when a decorator has been overriden then the location of its occurence stays the same or moves down the current loc
    # TODO: make this one-liner
    def _set_curr_cls(self, monkey_cls, bases, monkey_attrs):
        for attr, attr_val in monkey_attrs.items():
            decorated_with = getattr(attr_val, NamespacesConsts.DECORATED_WITH, None)
            if decorated_with != None:
                # attr_val in here is a decorated method
                for decorator in decorated_with:
                    monkey_cls.__map__[NamespacesConsts.BUILD][NamespacesConsts.DECORATORS].append(decorator)

    def run_bases(self, monkey_cls, bases, monkey_attrs):
        monkey_cls.__map__[NamespacesConsts.BUILD].setdefault(NamespacesConsts.DECORATORS, [])
        super(DecoratorMainComponent, self).run_bases(monkey_cls, bases, monkey_attrs)
