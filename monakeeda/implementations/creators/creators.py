from typing import Union, Any

from monakeeda.utils import get_wanted_params, wrap_in_list
from monakeeda.consts import NamespacesConsts
from .base_decorator import BaseCreatorDecorator
from ..validators import Validator
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor


class CreateFrom(BaseCreatorDecorator):
    __prior_handler__ = Validator

    def __init__(self, wanted_data_member: str, from_keys: Union[list, str] = '*'):
        super(CreateFrom, self).__init__(wanted_data_member)
        self.from_keys = wrap_in_list(from_keys)

    def build(self, monkey_cls, bases, monkey_attrs):
        super(CreateFrom, self).build(monkey_cls, bases, monkey_attrs)

        monkey_cls.__map__[NamespacesConsts.FIELDS][self.wanted_data_member][NamespacesConsts.DEPENDENCIES].extend(self.from_keys)

        if self.from_keys[0] == '*':
            for key in monkey_cls.__map__[NamespacesConsts.FIELDS]:
                if key != self.wanted_data_member:
                    monkey_cls.__map__[NamespacesConsts.FIELDS].setdefault(key, {}).setdefault(NamespacesConsts.DEPENDENTS, []).append(self.wanted_data_member)
        else:
            for key in self.from_keys:
                monkey_cls.__map__[NamespacesConsts.FIELDS].setdefault(key, {}).setdefault(NamespacesConsts.DEPENDENTS, []).append(self.wanted_data_member)

    def wrapper(self, cls, kwargs, config, wanted_fields_info):
        if self.from_keys[0] == '*':
            return self.func(cls, kwargs, config)

        return self.func(cls, get_wanted_params(kwargs, self.from_keys), config)

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_create_from_decorator(self, context)


# class GenerateDynamically(BaseCreatorDecorator):
#     def __init__(self, wanted_data_member: str, factory: list):
#         self.factory = factory
#         super(GenerateDynamically, self).__init__(wanted_data_member)
#
#     def wrapper(self, cls, kwargs, values_initialized_info, config, wanted_fields_info):
#         prevailed_type = None
#         for _type in self.factory:
#             condition = self.factory[_type]
#             wanted_kws = get_wanted_params(kwargs, *inspect.signature(condition).parameters.keys())
#             if condition(**wanted_kws):
#                 prevailed_type = _type
#
#         return self.func(cls, prevailed_type, **kwargs)
