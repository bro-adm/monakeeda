# from typing import Any
#
# from monakeeda.base import Field, ExceptionsDict
# from .base_numeric_constraint import NumericConstraintFieldParameter, NumericConstraintFailedException
# from ..implemenations_base_operator_visitor import ImplementationsOperatorVisitor
#
#
# # @Field.parameter
# class LTNumericConstraintFieldParameter(NumericConstraintFieldParameter):
#     __key__ = "lt"
#     __label__ = "lt_constraint"
#
#     def _handle_values(self, model_instance, values, stage, exceptions: ExceptionsDict):
#         value = values[self._field_key]
#
#         if value >= self.param_val:
#             exceptions[self.scope].append(NumericConstraintFailedException(self, self.param_val, value))
#
#     def accept_operator(self, operator_visitor: ImplementationsOperatorVisitor, context: Any):
#         pass
#
#
