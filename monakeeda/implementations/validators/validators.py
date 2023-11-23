from typing import Any, Union

from monakeeda.base import ExceptionsDict
from monakeeda.consts import NamespacesConsts
from monakeeda.utils import get_wanted_params, wrap_in_list
from .base_decorator import BaseValidatorDecorator
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..known_builders import DependenciesBuilder
from ..valid_values import ValidValues


class Validator(BaseValidatorDecorator):
    __prior_handler__ = ValidValues
    __builders__ = [DependenciesBuilder()]

    def __init__(self, field_key: str, dependencies: Union[list, str] = None):
        super(Validator, self).__init__(field_key)
        self.dependencies = wrap_in_list(dependencies) if dependencies else []

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        configs = getattr(model_instance, NamespacesConsts.STRUCT)[NamespacesConsts.CONFIGS]
        fields_info = getattr(model_instance, NamespacesConsts.STRUCT)[NamespacesConsts.FIELDS]

        wanted_fields = [self._field_key, *self.dependencies]
        result = self.func(model_instance, configs, get_wanted_params(fields_info, wanted_fields), get_wanted_params(values, wanted_fields))

        if result:
            if not isinstance(result, Exception):
                raise TypeError(f"{self.representor} requires a return of either None or an Exception instance but received {result}")
            else:
                exceptions[self.scope].append(result)

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_validator_decorator(self, context)
