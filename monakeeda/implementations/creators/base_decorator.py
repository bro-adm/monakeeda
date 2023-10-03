from abc import ABC

from monakeeda.consts import NamespacesConsts
from monakeeda.base import BaseDecorator


class BaseCreatorDecorator(BaseDecorator, ABC):
    __label__ = 'creator'

    def __init__(self, wanted_data_member: str):
        self.wanted_data_member = wanted_data_member

    def handle_values(self, model_instance, values, stage) -> dict:
        fields_info = model_instance.__map__[NamespacesConsts.FIELDS]
        wanted_val = self.wrapper(model_instance, values, model_instance.__map__[NamespacesConsts.BUILD][NamespacesConsts.CONFIG], fields_info[self.wanted_data_member])

        return {self.wanted_data_member: wanted_val}

    def build(self, monkey_cls, bases, monkey_attrs):
        monkey_cls.__map__[NamespacesConsts.FIELDS].setdefault(self.wanted_data_member, {}).update({NamespacesConsts.CREATOR: self, NamespacesConsts.DEPENDENCIES: []})
