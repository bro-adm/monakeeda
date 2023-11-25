# from abc import ABC
# from typing import Union
#
# from monakeeda.base import Component, FieldParameter, BaseModel
# from ..known_builders import ParameterValueTypeValidator, CoreAnnotationsExtractor
# from ..discriminator import Discriminator
# from ..cast import Cast
#
#
# class NumericConstraintFieldParameter(FieldParameter, ABC):
#     __builders__ = [ParameterValueTypeValidator((int, float)), CoreAnnotationsExtractor(int, float)]
#     # __builders__ = [ParameterValueTypeValidator((int, float)), CoreAnnotationsExtractor(Cast)]
#
#
# class NumericConstraintFailedException(ValueError):
#     def __init__(self, component: Component, constraint_value: Union[int, float], provided_value: Union[int, float]):
#         self.component_representor = component.representor
#         self.constraint_value = constraint_value
#         self.provided_value = provided_value
#
#     def __str__(self):
#         return f"{self.component_representor} constraint of {self.constraint_value} not matched -> provided {self.provided_value}"
