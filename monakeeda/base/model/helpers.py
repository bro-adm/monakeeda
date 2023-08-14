import inspect


def ignore_unwanted_params(cls, kwargs):
    wanted_kwargs = {}
    sig_params = inspect.signature(cls).parameters
    for param_key in list(sig_params.keys()):
        if param_key in kwargs.keys():
            wanted_kwargs[param_key] = kwargs[param_key]
    return wanted_kwargs


def add_defaults(cls, wanted_kwargs):
    params = inspect.signature(cls).parameters
    for param_name in params:
        if param_name not in wanted_kwargs:
            wanted_kwargs[param_name] = params[param_name]._default
    return wanted_kwargs
