from abc import ABC

from monakeeda.consts import NamespacesConsts, FieldConsts
from monakeeda.base import BaseDecorator


class BaseCreatorDecorator(BaseDecorator, ABC):
    __label__ = 'creator'

    def __init__(self, wanted_data_member: str):
        self.wanted_data_member = wanted_data_member

    def handle_values(self, model_instance, values, stage) -> dict:
        fields_info = getattr(model_instance, NamespacesConsts.STRUCT)[NamespacesConsts.FIELDS]
        wanted_val = self.wrapper(model_instance, values, getattr(model_instance, NamespacesConsts.STRUCT)[NamespacesConsts.CONFIG], fields_info[self.wanted_data_member])

        return {self.wanted_data_member: wanted_val}

    def build(self, monkey_cls, bases, monkey_attrs):
        # setdefault is in use because this can be set on a none schema parameter
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS].setdefault(self.wanted_data_member, {}).update({FieldConsts.CREATOR: self, FieldConsts.DEPENDENCIES: []})
