# from abc import ABC, abstractmethod
#
# from monakeeda.consts import NamespacesConsts
# from monakeeda.utils import set_default_attr_if_does_not_exist
# from ..component import Component
#
# """
# This is based upon the understanding of decorators in class implementation, and add on it with making it abstract :)
#
# When implementing a decorator thta inherits from the BaseDecorator class, you are calling your implemented __init__
# method, the __call__ method which is set in the abstract class is the decorator in action that runs
# your needs according to the standard set in the base class via its abstract method (SOLID abstractions)
#
# An important note, is to understand that these decorators happen at initialization time and run the methods they decorate.
# In the case below, the lol method will be called in the class instance initialization stage
# and the parameters will be passed to it according to your decorator implemtnation.
# Same thing regarding the effects of the decorator on values, etc...
#
# @Decorator(x, y, z) -> calls the __init__
# def lol(ClsType, ...):
#     ........
#
# if you don't want the decorator to get params and do @Decorator -> without initializing it
# don't do and __init__ function -> like making one that does not receive params
#
# Remember decorators run at code load time -> this is used here when you understand the fact that the __call__ method
# will run on load time, making all the methods in the class decorated be marked and ready for use in model instance initialization
#
# """
#
#
# class BaseDecorator(Component, ABC):
#     @abstractmethod
#     def wrapper(self, monkey_cls, kwargs, values_initialized_info, config, wanted_fields_info):
#         """
#
#         :param monkey_cls: model ClsType
#         :param kwargs: kwargs given in model init (aka data members)
#         :param values_initialized_info: all the values initialized info
#         :params config: model config
#         :param wanted_fields_info: the fields required for decorator operation
#
#         :return: decorated func result
#         """
#         pass
#
#     def _set_func_landscape(self):
#         # Adds the decorator class instance to the function attributes for further usage in the DecoratorMainComponent
#         getattr(self.func, NamespacesConsts.DECORATED_WITH).append(self)
#
#     def __call__(self, func):
#         """
#         :Warning: make sure to understand how decorators are found and run IF altering this method
#         """
#
#         self.func = func
#         set_default_attr_if_does_not_exist(self.func, NamespacesConsts.DECORATED_WITH, [])
#         self._set_func_landscape()
#
#         return func
