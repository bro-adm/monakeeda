import collections
from typing import Any


def get_wanted_params(kwargs: dict, keys: list):
    return {key: kwargs[key] for key in keys}


def wrap_in_list(x: Any):
    if type(x) not in [tuple, list]:
        return [x]

    return x


def set_default_attr_if_does_not_exist(obj, name, default_val):
    # like setdefault for dict but for obj Attrs
    setattr(obj, name, getattr(obj, name, default_val))


def insert_if_does_not_exists(key, new_val, the_dict):
    if key not in the_dict:
        the_dict[key] = new_val


def deep_update(source, overrides):
    """
    Update a nested dictionary or similar mapping.
    Modify ``source`` in place.
    """

    for key, value in overrides.items():
        if isinstance(value, collections.Mapping) and value:
            returned = deep_update(source.get(key, {}), value)
            source[key] = returned
        else:
            source[key] = overrides[key]

    return source


def more_than_one_key_in_dict(the_dict: dict, keys: list):
    one_key_in_dict = False

    for key in keys:
        if key in the_dict:
            if one_key_in_dict:
                return True
            one_key_in_dict = True

    return False


def get_ordered_set_list(seq) -> list:
    # TODO: check why did I do this like this :(

    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]
