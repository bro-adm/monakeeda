# from monakeeda.consts import NamespacesConsts, FieldConsts
# from .base_fields import Field, FieldParameter
# from ..component import Stages
# from ..config import Config
#
#
# @Field.parameter
# class DefaultParameter(FieldParameter):
#     __key__: str = 'default'
#     __label__ = 'default_provider'
#     __prior_handler__ = Config
#
#     def handle_values(self, model_instance, values, stage) -> dict:
#         if stage == Stages.INIT:
#             return {self._field_key: values.get(self._field_key, self.param_val)}
#
#         return {}
#
#     def build(self, monkey_cls, bases, monkey_attrs):
#         super(DefaultParameter, self).build(monkey_cls, bases, monkey_attrs)
#         monkey_cls.__map__[NamespacesConsts.FIELDS][self._field_key][FieldConsts.REQUIRED] = False
