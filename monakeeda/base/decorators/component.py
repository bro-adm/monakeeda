from typing import List

from monakeeda.consts import NamespacesConsts
from .base_decorator import BaseDecorator
from ..component import MainComponent


class DecoratorMainComponent(MainComponent[BaseDecorator]):

    @property
    def _components(self) -> List[BaseDecorator]:
        return self._monkey_cls.__map__[NamespacesConsts.BUILD][NamespacesConsts.DECORATORS]

    # TODO: validate run order preserves method order
    def values_handler(self, key, model_instance, values) -> dict:
        """
        A single decorator component can run on all model fields.
        specific white/black lists can be set according to decorator implementations and instances configurations.

        Therefore, the values_handler logic is set by allowing each decorator to run its values_handler for all fields.
        This is the opposite from other implementation.
        """
        for decorator in model_instance.__map__[NamespacesConsts.BUILD][NamespacesConsts.DECORATORS]:
            values = decorator.values_handler(key, model_instance, values)

        return values

    # TODO: fix the issue that happens when overriden -> investigate!!!
    def _set_by_base(self, monkey_cls, base, attrs):
        monkey_cls.__map__[NamespacesConsts.BUILD][NamespacesConsts.DECORATORS].extend(
            base.__map__[NamespacesConsts.BUILD][NamespacesConsts.DECORATORS])

    # TODO: decide if when a decorator has been overriden then the location of its occurence stays the same or moves down the current loc
    def _set_curr_cls(self, monkey_cls, bases, monkey_attrs):
        for attr, attr_val in monkey_attrs.items():
            decorated_with = getattr(attr_val, NamespacesConsts.DECORATED_WITH, None)
            if decorated_with != None:
                # attr_val in here is a decorated method
                for decorator in decorated_with:
                    decorator.build(monkey_cls, bases, monkey_attrs)
                    monkey_cls.__map__[NamespacesConsts.BUILD][NamespacesConsts.DECORATORS].append(decorator)

    def _set_cls_landscape(self, monkey_cls, bases, monkey_attrs):
        monkey_cls.__map__[NamespacesConsts.BUILD].setdefault(NamespacesConsts.DECORATORS, [])
        super(DecoratorMainComponent, self)._set_cls_landscape(monkey_cls, bases, monkey_attrs)
