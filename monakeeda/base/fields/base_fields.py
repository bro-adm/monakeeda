from abc import ABC

from monakeeda.consts import FieldConsts, NamespacesConsts
from ..component import ConfigurableComponent, Parameter


class FieldParameter(Parameter, ABC):

    def __init__(self, param_val):
        self._field_key = None
        super().__init__(param_val)

    def _set_cls_landscape(self, monkey_cls, bases, monkey_attrs):
        monkey_cls.__map__[NamespacesConsts.FIELDS][self._field_key][self.__key__] = self.param_val


class Field(ConfigurableComponent[FieldParameter]):
    pass


class NoField(Field, copy_parameter_components=False):
    """
    copy_parameter_components=False -> will keep the same list memory context as the Field Component itself ->
    meaning all the parameters available to it will be available here which is important for cases parameter
    initializations are added by code and not user like alias in AliasGenerator.
    """

    def __init__(self):
        # hard set: no params available for initialization
        super(NoField, self).__init__()

    def _set_cls_landscape(self, monkey_cls, bases, monkey_attrs):
        super(NoField, self)._set_cls_landscape(monkey_cls, bases, monkey_attrs)
        monkey_cls.__map__[NamespacesConsts.FIELDS][self._field_key][FieldConsts.REQUIRED] = True
