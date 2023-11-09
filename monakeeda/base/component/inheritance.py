# from enum import Enum
# from typing import List, Tuple
#
# from .parameter_component import Parameter
#
#
# class Inheritance(Enum):
#     OVERRIDE = 'override'
#     APPEND = 'append'
#     IGNORE = 'ignore'
#     KEEP = 'keep'
#
#
# def manage_inheritance(current_parameters: List[Parameter], new_parameters: List[Parameter], is_bases=False, previous_collisions:List[str]=None) -> Tuple[List[Parameter], List[str]]:
#     """
#     Meant for use with the ComponentManagers, in which we have the set by base and set curr cls.
#     Each method has the responsibility to manage inheritance itself on the relevant components under its jurisdiction.
#
#     This is a helper method to do just that whilst acknowledging the fact that the merge order is from the bases up to the current main cls.
#
#     What can happen with inheritance is either bases collision parameters or main cls overrideable parameters - THERE ARE NO APPEND PARAMETERS.
#     What we dont want to happen is to change the configurations of the fields from the inherited classes
#
#     to keep context of previous collision on bases merges you pass the previous_collisions value.
#     the value for it is provided via this method on return
#
#     each parameter lists will not hold in themselves more than one of the same __key__.
#
#     :returns: Merged Parameters, Collision Parameters Keys
#     """
#
#     merged_parameters = new_parameters.copy()
#     all_collision_parameters_keys = []
#
#     # remove previous collisions on bases merges
#     if is_bases and previous_collisions:
#         for collision_parameter_key in previous_collisions:
#             for parameter in merged_parameters:
#                 if parameter.__key__ == collision_parameter_key:
#                     merged_parameters.remove(parameter)
#                     break
#
#     for current_parameter in current_parameters:
#         add_current = True
#
#         for new_parameter in merged_parameters:
#             if new_parameter.__key__ == current_parameter.__key__:
#                 add_current = False
#
#                 if is_bases:
#                     merged_parameters.remove(new_parameter)
#                     all_collision_parameters_keys.append(new_parameter.__key__)
#
#                 break
#
#         if add_current:
#             merged_parameters.append(current_parameter)
#
#     return merged_parameters, all_collision_parameters_keys
#
