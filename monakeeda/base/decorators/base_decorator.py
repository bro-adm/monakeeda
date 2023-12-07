from abc import ABC

from monakeeda.consts import DecoratorConsts
from monakeeda.utils import set_default_attr_if_does_not_exist
from ..component import Component


class BaseDecorator(Component, ABC):
    """
    The Decorators concept is that they are fully initialized by the user and like the responsibility of an actual decorator,
    they only wrap the actual client set logic whilst restricting responsibility like extracting relevant information and managing results.

    The init method is saved for each Decorator implementation to implement.
    The __call__ method is pre implemented to set the known namespace that the Decorator Manager looks for on Monakeeda decorated methods.
    """

    def __init__(self, field_key: str):
        super().__init__()
        self._field_key = field_key

    @property
    def representor(self) -> str:
        return self.__class__.__name__

    @property
    def scope(self) -> str:
        return self._field_key

    def _set_func_landscape(self):
        # Adds the decorator class instance to the function attributes for further usage in the DecoratorMainComponent
        getattr(self.func, DecoratorConsts.DECORATED_WITH).append(self)

    def __call__(self, func):
        """
        :Warning: make sure to understand how decorators are found and run IF altering this method
        """

        self.func = func
        set_default_attr_if_does_not_exist(self.func, DecoratorConsts.DECORATED_WITH, [])
        self._set_func_landscape()

        return func
