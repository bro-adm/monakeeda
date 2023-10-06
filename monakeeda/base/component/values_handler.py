from abc import ABC, abstractmethod
from typing import Union


class ValuesHandler(ABC):
    @abstractmethod
    def handle_values(self, model_instance, values, stage) -> Union[Exception, None]:
        pass
