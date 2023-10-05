from monakeeda.base import BaseModel
from monakeeda.consts import NamespacesConsts
from .schema import SchemaOperatorVisitor


class MonkeyModel(BaseModel):
    @classmethod
    def schema(cls) -> dict:
        model_schema = cls.__map__[NamespacesConsts.FIELDS].copy()
        cls._operate(cls, SchemaOperatorVisitor.__type__, model_schema)

        return model_schema
