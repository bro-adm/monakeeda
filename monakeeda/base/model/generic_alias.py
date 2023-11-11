from typing import _GenericAlias as TypingGenericAlias
from monakeeda.consts import NamespacesConsts, TmpConsts


class MonkeyGenericAlias(TypingGenericAlias, _root=True):

    @classmethod
    def init_from_typing_generic_alias(cls, typing_generic_alias: TypingGenericAlias):
        return cls(typing_generic_alias.__origin__, typing_generic_alias.__args__)

    def __call__(self, *args, **kwargs):
        getattr(self.__origin__, NamespacesConsts.TMP)[TmpConsts.GENERICS] = self.__args__
        return super().__call__(*args, **kwargs)
