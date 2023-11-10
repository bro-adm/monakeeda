from typing import Union, Any

from monakeeda.utils import get_wanted_params, wrap_in_list
from monakeeda.consts import NamespacesConsts, FieldConsts
from .base_decorator import BaseCreatorDecorator
from ..missing import ValidateMissingFieldsConfigParameter
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from monakeeda.base import NoField


class CreateFrom(BaseCreatorDecorator):
    __prior_handler__ = ValidateMissingFieldsConfigParameter

    def __init__(self, field_key: str, from_keys: Union[list, str] = '*'):
        super(CreateFrom, self).__init__(field_key)
        self.from_keys = wrap_in_list(from_keys)

    def build(self, monkey_cls, bases, monkey_attrs):
        super(CreateFrom, self).build(monkey_cls, bases, monkey_attrs)

        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.DEPENDENCIES].extend(self.from_keys)

        # dependency key-values can be none schema parameters - therefore setdeafult is in use
        if self.from_keys[0] == '*':
            for key in monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS]:
                if key != self._field_key:
                    monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS].setdefault(key, {}).setdefault(FieldConsts.DEPENDENTS, []).append(self._field_key)
                    monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS].setdefault(key, {}).setdefault(FieldConsts.COMPONENTS, [])
        else:
            for key in self.from_keys:
                monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS].setdefault(key, {})
                monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][key].setdefault(FieldConsts.DEPENDENTS, []).append(self._field_key)
                monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][key].setdefault(FieldConsts.COMPONENTS, [])
                monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][key][FieldConsts.REQUIRED] = True
                no_field = NoField.override_init(key, [], {})
                monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][key].setdefault(FieldConsts.FIELD, no_field)

    def _handle_values(self, model_instance, values, stage):
        fields_info = getattr(model_instance, NamespacesConsts.STRUCT)[NamespacesConsts.FIELDS]
        configs = getattr(model_instance, NamespacesConsts.STRUCT)[NamespacesConsts.CONFIGS]

        wanted_val = self.wrapper(model_instance, values, configs, fields_info)
        values[self._field_key] = wanted_val

    def wrapper(self, monkey_cls, values, configs, fields_info):
        if self.from_keys[0] == '*':
            return self.func(monkey_cls, values, configs, fields_info)

        return self.func(monkey_cls, configs, get_wanted_params(fields_info, self.from_keys), get_wanted_params(values, self.from_keys))

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
