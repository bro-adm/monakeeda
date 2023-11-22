from typing import List, Any, Union

from monakeeda.base import ExceptionsDict
from monakeeda.consts import NamespacesConsts
from monakeeda.utils import get_wanted_params
from .base_decorator import BaseValidatorDecorator
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from ..valid_values import ValidValues


class Validator(BaseValidatorDecorator):
    __prior_handler__ = ValidValues

    def __init__(self, field_key: str, dependencies: List[str] = None):
        super(Validator, self).__init__(field_key)
        self.dependencies = dependencies if dependencies else []

    def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
        configs = getattr(model_instance, NamespacesConsts.STRUCT)[NamespacesConsts.CONFIGS]
        fields_info = getattr(model_instance, NamespacesConsts.STRUCT)[NamespacesConsts.FIELDS]

        wanted_fields = [self._field_key, *self.dependencies]
        result = self.func(model_instance, configs, get_wanted_params(fields_info, wanted_fields), get_wanted_params(values, wanted_fields))

        if result:
            exceptions[self._field_key].append(result)

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_validator_decorator(self, context)
