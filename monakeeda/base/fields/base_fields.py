from abc import ABC

from monakeeda.consts import FieldConsts, NamespacesConsts
from ..component import ConfigurableComponent, Parameter


class FieldParameter(Parameter, ABC):

    def __init__(self, field_key: str, param_val):
        self._field_key = field_key
        super().__init__(param_val)

    def _set_cls_landscape(self, monkey_cls, bases, monkey_attrs):
        super()._set_cls_landscape(monkey_cls, bases, monkey_attrs)
        monkey_attrs[NamespacesConsts.FIELDS][self._field_key][self.__key__] = self.param_val


class Field(ConfigurableComponent[FieldParameter]):

    def __init__(self, field_key: str, **params):
        self._field_key = field_key
        super().__init__(**params)

    def __initiate_params(self, params: dict):
        for param_key, param_val in params.items():
            for possible_param in self.__parameters_components__:
                if param_key == possible_param.__key__:
                    self._initialized_params.append(possible_param(self._field_key, param_val))
                    break

    def _set_cls_landscape(self, monkey_cls, bases, monkey_attrs):
        super(Field, self)._set_cls_landscape(monkey_cls, bases, monkey_attrs)
        monkey_attrs[NamespacesConsts.FIELDS][self._field_key][FieldConsts.FIELD] = self


class NoField(Field, copy_parameter_components=False):
    """
    copy_parameter_components=False -> will keep the same list memory context as the Field Component itself ->
    meaning all the parameters available to it will be available here which is important for cases parameter
    initializations are added by code and not user like alias in AliasGenerator.
    """

    def __init__(self, field_key):
        # hard set: no params available for initialization
        super(NoField, self).__init__(field_key)

    def _set_cls_landscape(self, monkey_cls, bases, monkey_attrs):
        super(NoField, self)._set_cls_landscape(monkey_cls, bases, monkey_attrs)
        monkey_attrs[FieldConsts.REQUIRED] = True
