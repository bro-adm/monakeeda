import inspect
from collections import defaultdict


class defaultdictvalue(defaultdict):
    """
    A regular defaultdict gets a non input lambda to generate the default value.

    This one get the key as an input to generate a custom output for each key
    """

    def __missing__(self, key):
        """
        __missing__(key) # Called by __getitem__ for missing key
        """

        self[key] = value = self.default_factory(key)
        return value


def get_cls_attrs(cls) -> dict:
    # returns only custom cls attrs (not the base python ones) -> if do not interfere with python cls parameters style
    attrs = inspect.getmembers(cls, lambda a: not (inspect.isroutine(a)))

    new_attrs = dict({tup[0]: tup[1] for tup in attrs}['__dict__'])
    new_attrs = {key: val for key, val in new_attrs.items() if not key.startswith('_')}

    for tup in attrs:
        if not tup[0].startswith('_'):
            new_attrs[tup[0]] = tup[1]

    return new_attrs
