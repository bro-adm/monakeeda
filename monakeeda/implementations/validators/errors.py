from typing import List


class ValidatorReturnedErrorsException(Exception):
    def __init__(self, name, exceptions: List[Exception]):
        self.name = name
        self.exceptions = exceptions

    def __str__(self):
        return f"Validator {self.name} returned the following errors {self.exceptions}"
