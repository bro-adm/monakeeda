from typing import Dict, Any, Tuple, List, Union, Type

from monakeeda.base import BaseMonkey, Field
from monakeeda.consts import NamespacesConsts, PythonNamingConsts
from .implementations import OpenAPIOperatorVisitor


class MonkeyModel(BaseMonkey):
    @classmethod
    def openapi(cls) -> dict:
        model_schema = getattr(cls, NamespacesConsts.FIELDS).copy()
        cls._operate(cls, OpenAPIOperatorVisitor.__type__, model_schema)

        return model_schema

    class Config:
        validate_missing_fields = True


def generate_model(name: str, fields: Dict[str, Union[Field, Any]]=None, annotations: Dict[str, Any]=None, configs: Dict[str, type]=None, decorators: List[callable]=None, bases: Tuple[BaseMonkey]=None) -> Type[MonkeyModel]:
    bases = bases if bases else (MonkeyModel,)

    attrs = {}
    attrs.update(fields if fields else {})
    attrs[PythonNamingConsts.annotations] = annotations if annotations else {}
    attrs.update(configs if configs else {})
    attrs.update({func.__name__: func for func in decorators} if decorators else {})

    return type(name, bases, attrs)
