from typing import List

from typing_extensions import get_origin

# TODO: try to delete this dictionary
__helper_mapping = {list: List}


def get_type_cls(tp):
    origin = get_origin(tp)
    if origin:
        if type(origin) == type:
            return __helper_mapping[origin]
        return origin
    return tp
