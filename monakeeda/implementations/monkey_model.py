from monakeeda.base import BaseModel
from monakeeda.consts import NamespacesConsts
from .schema import OpenAPIOperatorVisitor


class MonkeyModel(BaseModel):
    @classmethod
    def openapi(cls) -> dict:
        model_schema = getattr(cls, NamespacesConsts.FIELDS).copy()
        cls._operate(cls, OpenAPIOperatorVisitor.__type__, model_schema)

        return model_schema
