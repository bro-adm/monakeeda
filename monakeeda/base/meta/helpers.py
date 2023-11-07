def handle_class_inputs(cls, bases, **inputs):
    """
    class A(Model, a=9, ...):
        ...

    cls.__a__ = 9

    if not provided takes from base 0 (a model), and if does not have bases (direct metaclass user) raises required setup
    """

    if not bases:
        unset_inputs = [key for key, val in inputs.items() if val is None]

        if unset_inputs:
            raise ValueError(f'direct metaclass users needs to pass {unset_inputs} inputs')

        for key, val in inputs.items():
            setattr(cls, f"__{key}__", val)

    else:
        for key, val in inputs.items():
            attr_name = f"__{key}__"
            setattr(cls, attr_name, val if val else getattr(bases[0], attr_name))
