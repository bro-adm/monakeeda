from typing import List, Dict

from typing_extensions import get_origin

__helper_mapping = {list: List, dict: Dict}


def get_type_cls(tp):
    origin = get_origin(tp)
    if origin:
        if type(origin) == type:
            return __helper_mapping[origin]
        return origin
    return tp


def type_validation(value, types):
    if not isinstance(value, types):
        return TypeError(f'{value} needs to be of type/s {types}')

    return
