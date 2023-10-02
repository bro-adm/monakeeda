from abc import ABC, abstractmethod
from enum import Enum


class Stages(Enum):
    INIT = 'init'
    UPDATE = 'update'


class ValuesHandler(ABC):
    @abstractmethod
    def handle_values(self, model_instance, values, stage) -> dict:
        pass
