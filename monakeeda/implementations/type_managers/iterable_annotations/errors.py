from typing import List
from monakeeda.utils import capitalize_words


class ItemException(Exception):
    def __init__(self, main_type: type, compartment, exception: Exception):
        self.main_type = main_type
        self.compartment = compartment
        self.exception = exception

    def __str__(self):
        return f"{capitalize_words(self.main_type.__name__)} (compartment={self.compartment}) -> {self.exception}"
