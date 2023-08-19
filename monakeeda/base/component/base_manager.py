from abc import ABC, abstractmethod


class BaseManager(ABC):
    @abstractmethod
    def _set_by_base(self, monkey_cls, base, monkey_attrs):
        pass

    @abstractmethod
    def _set_curr_cls(self, monkey_cls, bases, monkey_attrs):
        pass

    def run_bases(self, monkey_cls, bases, monkey_attrs):
        for base in bases:
            self._set_by_base(monkey_cls, base, monkey_attrs)

        self._set_curr_cls(monkey_cls, bases, monkey_attrs)
