from typing import _GenericAlias as TypingGenericAlias

from monakeeda.consts import NamespacesConsts, TmpConsts
from monakeeda.logger import logger, STAGE, MONKEY


class MonkeyGenericAlias(TypingGenericAlias, _root=True):
    """
    Python generics are weird.

    When one sets the actual generic types on a generic class, it calls the Generic __class_getitem__ method.
    That method returns a _GenericAlias.
    When you initialize YOUR class it actually calls the __call__ method of the _GenericAlias.

    For Monakeeda generics are actually important not for just type hinting as one can imagine.
    The methodology is to keep their current state in the TMP context and we need to load it via this __call__ method for some initialization cases.

    The Model overrides the Generic __class_getitem__ method to return an instance of this class instead of the _GenericAlias.

    For the full list of initialization cases that need to be acknowledged by our generics TMP context read the advanced docs.
    """

    @classmethod
    def init_from_typing_generic_alias(cls, typing_generic_alias: TypingGenericAlias):
        return cls(typing_generic_alias.__origin__, typing_generic_alias.__args__)

    def __call__(self, *args, **kwargs):
        getattr(self.__origin__, NamespacesConsts.TMP)[TmpConsts.GENERICS] = self.__args__

        logger.info(f"Init Scope Generics = {self.__args__}", extra={STAGE: "Monkey Generics", MONKEY: self.__origin__.__name__})

        return super().__call__(*args, **kwargs)
