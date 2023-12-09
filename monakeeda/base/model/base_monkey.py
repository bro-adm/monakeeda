from typing import Any, Generic

from monakeeda.consts import NamespacesConsts, TmpConsts
from monakeeda.logger import logger, STAGE, MONKEY
from monakeeda.utils import deep_update
from .errors import MonkeyValuesHandlingException
from .generic_alias import MonkeyGenericAlias
from .monkey_components_organizer import MonkeyComponentsOrganizer
from .monkey_scopes_manager import MonkeyScopesManager
from ..annotations import AnnotationManager, annotation_mapping
from ..component import get_run_decorator, labeled_components
from ..config import ConfigManager, all_configs
from ..decorators import DecoratorManager
from ..exceptions_manager import ExceptionsDict
from ..fields import FieldManager, Field, NoField
from ..interfaces import Stages
from ..meta import MonkeyMeta
from ..operator import all_operators

component_managers = [ConfigManager(all_configs), FieldManager(Field, NoField), DecoratorManager(), AnnotationManager(annotation_mapping)]


class BaseMonkey(metaclass=MonkeyMeta, component_managers=component_managers, scopes_manager=MonkeyScopesManager(), component_organizer=MonkeyComponentsOrganizer(labeled_components), operators_visitors=all_operators):
    """
    Responsible for holding the PURE run of all the logics combined without being dependent on any specific compartment.

    Supplies the API for further extensions (e.g. _operate)

    Also Responsible for managing python's weird shticks (e.g. generics -> __class_getitem__)
    """

    def __class_getitem__(cls, item):
        generic = super().__class_getitem__(item)  # probably will only be called when actually Generic
        getattr(cls, NamespacesConsts.TMP)[TmpConsts.GENERICS] = generic.__args__

        logger.info(f"Class Scope Generics = {generic.__args__}", extra={STAGE: "Monkey Generics", MONKEY: cls.__name__})

        return MonkeyGenericAlias.init_from_typing_generic_alias(generic)

    @classmethod
    @property
    def struct(cls) -> dict:
        return getattr(cls, NamespacesConsts.STRUCT)

    @classmethod
    @property
    def scopes(cls) -> dict:
        return getattr(cls, NamespacesConsts.SCOPES)

    def _handle_values(self, values: dict, stage):
        super().__setattr__("__run_organized_components__", self.__class__.__run_organized_components__.copy())
        exceptions = ExceptionsDict()  # pass by reference - so updates will be available

        for component in self.__run_organized_components__.keys():
            decorators = get_run_decorator(component)
            if decorators:
                prior_handler = component
                for decorator in decorators:
                    decorator.component = prior_handler
                    prior_handler = decorator

                decorators[-1].handle_values(self, values, stage, exceptions)

            elif self.__run_organized_components__[component]:
                component.handle_values(self, values, stage, exceptions)

        if exceptions:
            raise MonkeyValuesHandlingException(self.__class__.__name__, values, exceptions)

        for key in values:
            super(BaseMonkey, self).__setattr__(key, values[key])

    def __init__(self, **kwargs):
        self.__notes__ = {}  # Used by components to write current known informations between stages at the scope of the model instance only
        self._handle_values(kwargs, Stages.INIT)

    def update(self, **kwargs):
        if Generic in self.__class__.mro():
            logger.info(f"Update Scope Generics = {self.__orig_class__.__args__}", extra={STAGE: "Monkey Generics", MONKEY: self.__class__.__name__})

        kwargs = deep_update(self.__dict__.copy(), kwargs)
        self._handle_values(kwargs, Stages.UPDATE)

    def __setattr__(self, key, value):
        if key in self.struct[NamespacesConsts.FIELDS]:
            # I know this does not catch random extras concept ->
            # but the other use case is to validate each type of external or internal setter logic (e.g. _TYPING_INTERNALS and extranal setters like DecoratorComponent)
            self.update(**{key: value})
        else:
            super().__setattr__(key, value)

    def __eq__(self, other):
        if not isinstance(other, BaseMonkey):
            raise NotImplementedError
        return self.__dict__ == other.__dict__

    # def __str__(self):
    #     return str(get_wanted_params(self.__dict__, self.struct[NamespacesConsts.FIELDS].keys()).values())

    # def __hash__(self):
    #     print(tuple(get_wanted_params(self.__dict__, self.struct[NamespacesConsts.FIELDS].keys()).values()))
    #     return hash(tuple(get_wanted_params(self.__dict__, self.struct[NamespacesConsts.FIELDS].keys()).values()))

    @staticmethod
    def _operate(model, operator_type: str, context: Any):
        operator_visitor = model.__operators_visitors__[operator_type]

        for component in model.__organized_components__:
            component.accept_operator(operator_visitor, context)
