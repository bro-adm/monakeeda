from typing import List, Any, Union

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

    def _handle_values(self, model_instance, values, stage) -> Union[Exception, None]:
        configs = getattr(model_instance, NamespacesConsts.STRUCT)[NamespacesConsts.CONFIGS]
        fields_info = getattr(model_instance, NamespacesConsts.STRUCT)[NamespacesConsts.FIELDS]

        return self.wrapper(model_instance, values, configs, fields_info)

    def wrapper(self, monkey_cls, values, configs, fields_info):
        wanted_fields = [self._field_key, *self.dependencies]
        return self.func(monkey_cls, configs, get_wanted_params(fields_info, wanted_fields), get_wanted_params(values, wanted_fields))

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_validator_decorator(self, context)
