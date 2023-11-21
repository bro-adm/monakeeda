from typing import Any


def get_wanted_params(kwargs: dict, keys: list):
    return {key: kwargs[key] for key in keys if key in kwargs}


def wrap_in_list(x: Any):
    if type(x) not in [tuple, list]:
        return [x]

    return x


def set_default_attr_if_does_not_exist(obj, name, default_val):
    # like setdefault for dict but for obj Attrs
    setattr(obj, name, getattr(obj, name, default_val))


def deep_update(source, overrides):
    """
    Update a nested dictionary or similar mapping.
    Modify ``source`` in place.
    """

    for key, value in overrides.items():
        if isinstance(value, dict) and value:
            returned = deep_update(source.get(key, {}), value)
            source[key] = returned
        else:
            source[key] = overrides[key]

    return source


def get_items_from_list(items: list, main_list: list) -> list:
    existing_items = []

    for item in items:
        if item in main_list:
            existing_items.append(item)

    return existing_items


def capitalize_words(input: str) -> str:
    parts = input.split('_')

    transformed_string = ' '.join(part.capitalize() for part in parts)

    return transformed_string
