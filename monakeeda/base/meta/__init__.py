"""
when creating a meta class there are some params given:
    __new__:
        objective - create and return the class itself -> a class in python is created only once when running the file
                    it is contained in with or without a main run
        when to use - use when in need of changing class attributed or when wanting to move the responsibility
                    of calling and understanding the meta data of a class and changing it accordingly
                    (like removing some of the bases of a class - no reason to do that)

        - name
        - bases -> extends from ... (recursive)
        - Attrs -> it gives all the other info that a class in python naturally sees ->
                annotated names (__annotations__ -> username: str -> __annotations__ = {'username': <class 'str'>}),
                all funcs (name, val), module info, default values, ... (class meta data)
        - **kwargs -> not needed to even given

    __init__:
        objective - ???
        when to use - ???

         - name
         - bases
         - Attrs

    __call__:
        calls both new and init funcs - useful for singletons and more ...

creating a meta class:
    - to create a meta class the class needs to extend from type or another metaclass.
    - BE CAREFUL - when creating a base class that holds that holds a custom metaclass you need that
                    all inheriting classes will only inherit from form classes with same base meta classes.
                    in this project I wanted to allow users to use the ABC class that uses the ABCMeta as its metaclass
                    so my custom metaclass inherits from ABCMeta

* __new__, __init__ and __call__ are funcs that all classes I think have (not sure about the __new__ func)
"""

from .mokey_meta import MonkeyMeta
from .organizers import ComponentOrganizer
