import json
from json import JSONDecodeError
from typing import Any

from pathvalidate import validate_filepath, ValidationError

from monakeeda.base import ConfigParameter, Config, ExceptionsDict, OperatorVisitor, Component
from monakeeda.utils import deep_update
from ..generators import AliasGenerator
from ..known_builders import ParameterValueTypeValidator


class FileInputException(Exception):
    def __init__(self, component: Component, exception: ValidationError):
        self.component_representor = component.representor
        self.exception = exception

    def __str__(self):
        return f"{self.component_representor} error -> {str(self.exception)} -> exception_type = {type(self.exception)}"


@Config.parameter
class FileInputConfigParameter(ConfigParameter):
    __key__ = "file_input"
    __prior_handler__ = AliasGenerator
    __builders__ = [ParameterValueTypeValidator(str)]

    @property
    def label(cls) -> str:
        return 'value_provider'

    @property
    def scope(self) -> str:
        return 'value_provider'

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        super()._build(monkey_cls, bases, monkey_attrs, exceptions, main_builder)

        try:
            validate_filepath(self.param_val)
        except ValidationError as e:
            exceptions[self.scope].append(FileInputException(self, e))

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        try:
            with open(self.param_val, 'r') as file:
                file_content = file.read()
                file_values = json.loads(file_content)

            deep_update(values, file_values)

        except (FileNotFoundError, JSONDecodeError) as e:
            exceptions[self.scope].append(FileInputException(self, e))

    def accept_operator(self, operator_visitor: OperatorVisitor, context: Any):
        pass
