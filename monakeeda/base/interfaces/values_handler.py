from abc import ABC, abstractmethod


class ValuesHandler(ABC):
    @abstractmethod
    def _handle_values(self, model_instance, values, stage):
        pass
