from abc import ABC

from monakeeda.consts import FieldConsts
from ..component import ConfigurableComponent, Parameter


class FieldParameter(Parameter, ABC):

    def _set_cls_landscape(self, monkey_cls, bases, monkey_attrs):
        super()._set_cls_landscape(monkey_cls, bases, monkey_attrs)
        monkey_attrs[self.__key__] = self.param_val


class Field(ConfigurableComponent[FieldParameter]):

    def _set_cls_landscape(self, monkey_cls, bases, monkey_attrs):
        super(Field, self)._set_cls_landscape(monkey_cls, bases, monkey_attrs)
        monkey_attrs[FieldConsts.FIELD] = self


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
        monkey_attrs[FieldConsts.REQUIRED] = True
