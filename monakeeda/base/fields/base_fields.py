from abc import ABC
from typing import Any, List, Dict

from monakeeda.consts import FieldConsts, NamespacesConsts
from monakeeda.helpers import ExceptionsDict
from ..component import Parameter, ConfigurableComponent
from ..operator import OperatorVisitor


class FieldParameter(Parameter, ABC):
    """
    Just like any other field scoped component, this one holds a _field_key attr as well.

    This component is known for the ability to be dynamically generated (e.g. Alias Generator generates Alias Parameters)
    To ensure no duplications of components, the __eq__ methodology is implemented.
    """

    def __init__(self, param_val, field_key):
        self._field_key = field_key
        super().__init__(param_val)

    def __eq__(self, other):
        if not isinstance(other, FieldParameter):
            return NotImplemented
        return self._field_key == other._field_key and self.param_val == other.param_val

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.COMPONENTS].append(self)


class Field(ConfigurableComponent[FieldParameter]):
    """
    Just like any other field scoped component, this one holds a _field_key attr as well.

    A sub class of the Configurable Component for allowing different managed Parameter Components list.

    Initialized via the Fields Manager, which itself acknowledges a set of Fields by default via the all_fields dictionary.
    Allows override of a Field class "type" by class name.
    """

    @classmethod
    def override_init(cls, field_key: str, parameters: List[FieldParameter], unused_params: Dict[str, Any]):
        instance = super().override_init(parameters, unused_params)
        instance._field_key = field_key

        return instance

    @classmethod
    def init_from_arbitrary_value(cls, value: Any):
        return cls(default=value)

    def _build(self, monkey_cls, bases, monkey_attrs, exceptions: ExceptionsDict, main_builder):
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.REQUIRED] = True
        monkey_attrs[NamespacesConsts.STRUCT][NamespacesConsts.FIELDS][self._field_key][FieldConsts.COMPONENTS].append(self)

    def _handle_values(self, model_instance, values, stage):
        pass

    def accept_operator(self, operator_visitor: OperatorVisitor, context: Any):
        operator_visitor.operate_field(self, context)


class NoField(Field, copy_parameter_components=False):
    """
    Not really special other then to represent via the name the fact that there is no Field for a specific attr.
    Allows the model run logics to run without any special if/else because the API stays the same.

    copy_parameter_components=False -> will keep the same list memory context as the Field Component itself ->
    meaning all the parameters available to it will be available here which is important for cases parameter
    initializations are added by code and not user like alias in AliasGenerator.
    """

    __prior_handler__ = Field

    def __init__(self):
        # hard set: no params available for initialization
        super(NoField, self).__init__()
