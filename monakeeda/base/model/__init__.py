"""
setting a meta class for a class and implementing a __init__, __call__ ... funcs does
not override the metaclass functions -> not like regular extension. a class that sets a metaclass can
still inherit from other classes as long as their meta classes come from the same base metaclass...
"""

from .base_model import MonkeyModel
