from abc import ABC
from typing import List

from monakeeda.base import BaseDecorator
from monakeeda.consts import NamespacesConsts, FieldConsts


class BaseValidatorDecorator(BaseDecorator, ABC):
    __label__ = 'validators'

    def __init__(self, data_members: List[str]):
        self.data_members = data_members

    def build(self, monkey_cls, bases, monkey_attrs):
        for dtm in self.data_members:
            # setdefault is in use because this can be set on a none schema parameter
            monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS].setdefault(dtm, {}).setdefault(FieldConsts.VALIDATORS, []).append(self)
