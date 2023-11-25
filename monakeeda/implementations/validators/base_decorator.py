from abc import ABC

from monakeeda.base import BaseDecorator


class BaseValidatorDecorator(BaseDecorator, ABC):
    @classmethod
    @property
    def label(cls) -> str:
        return "validations"

    def is_collision(self, other) -> bool:
        super().is_collision(other)
        return False
