from monakeeda.base import Parameter, MonkeyBuilder
from monakeeda.helpers import ExceptionsDict


class ParameterValueTypeNotAllowedException(Exception):
    def __init__(self, parameter: Parameter, wanted_type):
        self.parameter_key = parameter.__key__
        self.value = parameter.param_val
        self.wanted_type = wanted_type

    def __str__(self):
        return f"{self.parameter_key} accepts value of type {self.wanted_type}, but was provided with {self.value}"


class ParameterValueTypeValidator(MonkeyBuilder):
    def __init__(self, wanted_ype):
        self.wanted_type = wanted_ype

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder: Parameter):
        if not isinstance(main_builder.param_val, self.wanted_type):
            exception = ParameterValueTypeNotAllowedException(main_builder, self.wanted_type)
            exceptions[main_builder._field_key].append(exception)

