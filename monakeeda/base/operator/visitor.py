import inspect
from abc import ABC, abstractmethod
from typing import ClassVar, Generic, TypeVar

all_operators = {}

TOperatorContext = TypeVar('TOperatorContext')


class OperatorVisitor(ABC, Generic[TOperatorContext]):
    __type__: ClassVar[str]

    def __init_subclass__(cls):
        super().__init_subclass__()

        if not inspect.isabstract(cls):
            all_operators[cls.__type__] = cls()

    @abstractmethod
    def operate_field(self, field: 'Field', context: TOperatorContext):
        pass

    @abstractmethod
    def operate_config(self, config: 'Config', context: TOperatorContext):
        pass

    @abstractmethod
    def operate_model_annotation(self, annotation: 'ModelAnnotation', context: TOperatorContext):
        pass
