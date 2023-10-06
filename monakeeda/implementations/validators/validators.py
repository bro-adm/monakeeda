from typing import List, Any, Union

from monakeeda.utils import get_wanted_params
from monakeeda.consts import NamespacesConsts
from .base_decorator import BaseValidatorDecorator
from ..valid_values import ValidValues
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
from .errors import ValidatorReturnedErrorsException


class Validator(BaseValidatorDecorator):
    __prior_handler__ = ValidValues

    def __init__(self, data_members: List[str], dependencies: List[str] = None):
        super(Validator, self).__init__(data_members)
        self.dependencies = dependencies if dependencies else []

    def handle_values(self, model_instance, values, stage) -> Union[Exception, None]:
        config = getattr(model_instance, NamespacesConsts.STRUCT)[NamespacesConsts.CONFIG]
        fields_info = getattr(model_instance, NamespacesConsts.STRUCT)[NamespacesConsts.FIELDS]

        return self.wrapper(model_instance, values, config, fields_info)

    def wrapper(self, monkey_cls, values, config, fields_info):
        exceptions = []

        for key in self.data_members:
            wanted_fields = [key, *self.dependencies]
            result = self.func(monkey_cls, config, get_wanted_params(fields_info, wanted_fields), get_wanted_params(values, wanted_fields))

            if result:
                exceptions.append(result)

        return ValidatorReturnedErrorsException(self.func.__name__, exceptions) if exceptions else None

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        operator_visitor.operate_validator_decorator(self, context)
