from typing import List
from monakeeda.utils import capitalize_words


class ItemException(Exception):
    def __init__(self, main_type: type, compartment, exception: Exception):
        self.main_type = main_type
        self.compartment = compartment
        self.exception = exception

    def __str__(self):
        return f"{capitalize_words(self.main_type.__name__)} (compartment={self.compartment}) -> {self.exception}"

    def __eq__(self, other):
        if not isinstance(other, ItemException):
            raise ValueError(f"Exception provided not of type {self.__class__.__name__}")

        return self.main_type == other.main_type and self.compartment == other.compartment and str(self.exception) == str(other.exception)

    def __hash__(self):
        return hash((self.main_type, self.compartment, str(self.exception)))
