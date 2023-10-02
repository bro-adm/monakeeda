from abc import ABC, abstractmethod


class MonkeyBuilder(ABC):
    @abstractmethod
    def build(self, monkey_cls, bases, monkey_attrs):
        pass
