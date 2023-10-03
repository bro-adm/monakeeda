from abc import ABC

from monakeeda.base import BaseDecorator
from monakeeda.consts import NamespacesConsts


class BaseValidatorDecorator(BaseDecorator, ABC):
    __label__ = 'validators'

    def __init__(self, *data_members: str):
        self.data_members = data_members

    def handle_values(self, model_instance, values, stage) -> dict:
        fields_info = model_instance.__map__[NamespacesConsts.FIELDS]
        for dtm in self.data_members:
            self.wrapper(model_instance, values, model_instance.__map__[NamespacesConsts.BUILD][NamespacesConsts.CONFIG], fields_info[dtm])

        return {}

    def build(self, monkey_cls, bases, monkey_attrs):
        for dtm in self.data_members:
            monkey_cls.__map__[NamespacesConsts.FIELDS].setdefault(dtm, {}).setdefault(NamespacesConsts.VALIDATORS, []).append(self)
