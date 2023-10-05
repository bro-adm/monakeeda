from typing import List, Any

from monakeeda.utils import get_wanted_params
from .base_decorator import BaseValidatorDecorator
from ..valid_values import ValidValues
from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor


class Validator(BaseValidatorDecorator):
    __prior_handler__ = ValidValues

    def __init__(self, data_members: List[str], dependencies: List[str] = None):
        super(Validator, self).__init__(*data_members)
        self.dependencies = dependencies if dependencies else []

    def wrapper(self, cls, kwargs, config, wanted_fields_info):
        for key in self.data_members:
            self.func(cls, kwargs[key], wanted_fields_info, get_wanted_params(kwargs, self.dependencies))

    def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
        pass
