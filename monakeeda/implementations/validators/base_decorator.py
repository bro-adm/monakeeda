from abc import ABC

from monakeeda.base import BaseDecorator
from monakeeda.consts import NamespacesConsts, FieldConsts


class BaseValidatorDecorator(BaseDecorator, ABC):
    __label__ = 'validators'

    def __init__(self, *data_members: str):
        self.data_members = data_members

    def handle_values(self, model_instance, values, stage) -> dict:
        fields_info = getattr(model_instance, NamespacesConsts.STRUCT)[NamespacesConsts.FIELDS]
        config = getattr(model_instance, NamespacesConsts.STRUCT)[NamespacesConsts.CONFIG]

        for dtm in self.data_members:
            self.wrapper(model_instance, values, config, fields_info[dtm])

        return {}

    def build(self, monkey_cls, bases, monkey_attrs):
        for dtm in self.data_members:
            # setdefault is in use because this can be set on a none schema parameter
            monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS].setdefault(dtm, {}).setdefault(FieldConsts.VALIDATORS, []).append(self)
