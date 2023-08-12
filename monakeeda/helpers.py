import inspect
from collections import defaultdict


class defaultdictvalue(defaultdict):

    def __missing__(self, key):
        self[key] = value = self.default_factory(key)
        return value


# TODO: validate if in use
def get_param_default_from_signature(cls, key: str):
    params = inspect.signature(cls).parameters
    param = params.get(key, None)
    if param:
        return param._default

    return


def get_cls_attrs(cls) -> dict:
    # returns only custom cls attrs (not the base python ones) -> if do not interfere with python cls parameters style
    attrs = inspect.getmembers(cls, lambda a: not (inspect.isroutine(a)))
    new_attrs = dict({tup[0]: tup[1] for tup in attrs}['__dict__'])
    return {key: val for key, val in new_attrs.items() if not key.startswith('_')}
