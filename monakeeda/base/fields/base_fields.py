from abc import ABC

from monakeeda.consts import FieldConsts, NamespacesConsts
from ..component import ConfigurableComponent, Parameter, Stages


class FieldParameter(Parameter, ABC):

    def __init__(self, param_val):
        self._field_key = None
        super().__init__(param_val)

    def build(self, monkey_cls, bases, monkey_attrs):
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

    def build(self, monkey_cls, bases, monkey_attrs):
        super(NoField, self).build(monkey_cls, bases, monkey_attrs)
        monkey_cls.__map__[NamespacesConsts.FIELDS][self._field_key][FieldConsts.REQUIRED] = True


@Field.parameter
class DefaultParameter(FieldParameter):
    __key__: str = 'default'
    __label__ = 'default_provider'

    def handle_values(self, model_instance, values, stage) -> dict:
        if stage == Stages.INIT:
            return {self._field_key: values.get(self._field_key, self.param_val)}

        return {}

    def build(self, monkey_cls, bases, monkey_attrs):
        super(DefaultParameter, self).build(monkey_cls, bases, monkey_attrs)
        monkey_cls.__map__[NamespacesConsts.FIELDS][self._field_key][FieldConsts.REQUIRED] = False