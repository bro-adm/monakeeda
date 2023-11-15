from abc import ABC, abstractmethod

from monakeeda.consts import DecoratorConsts
from monakeeda.utils import set_default_attr_if_does_not_exist
from ..component import Component


class BaseDecorator(Component, ABC):
    @abstractmethod
    def wrapper(self, monkey_cls, values, config, fields_info):
        """

        :param monkey_cls: model ClsType
        :param kwargs: kwargs given in model init (aka data members)
        :params config: model config
        :param wanted_fields_info: the fields required for decorator operation

        :return: decorated func result
        """
        pass

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
