from typing import List, Dict, Optional

from typing_extensions import get_origin, get_args

__helper_mapping = {list: List, dict: Dict}


def get_type_cls(tp):
    """
    Gets a user set annotation -> from simple ones (e.g. str) to mid complex ones (e.g. List[str]) up to complex ones (e.g. Cast[str]).
    In other words, from native simple, to native mid up to custom complex annotations.

    for native simple annotations it returns the annotation itself.
    for native mid annotations it returns the typing object -> List[str] -> List
    for custom complex annotations it returns the custom annotation cls itself.

    This function is used in the AnnotationDefaultDict for getting the base type object/cls (e.g. str, List, Cast) from the user set annotation
    """

    origin = get_origin(tp)
    args = get_args(tp)

    if origin:  # all non generic types (e.g. list, dict, int, str) will not enter -> origin=None

        if type(origin) == type:  # all simple generics (e.g. Dict, List -> origin=dict, list accordingly) will enter
            return __helper_mapping[origin]

        elif len(args)==2 and type(None) in args:
            return Optional  # Optional sadly is equivalent to Union[X, None] - so needs an extra if

        return origin

    return tp


def type_validation(value, types):
    if not isinstance(value, types):
        return TypeError(f'{value} needs to be of type/s {types}')

    return
