from abc import ABC

from monakeeda.base import BaseDecorator


class BaseMutatorDecorator(BaseDecorator, ABC):
    @classmethod
    @property
    def label(cls) -> str:
        return "mutators"

    def is_collision(self, other) -> bool:
        super().is_collision(other)
        return False
