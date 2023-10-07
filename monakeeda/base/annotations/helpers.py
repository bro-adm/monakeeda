from typing import List, Dict, Optional

from typing_extensions import get_origin, get_args

__helper_mapping = {list: List, dict: Dict}


def get_type_cls(tp):
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
