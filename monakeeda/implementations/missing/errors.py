from typing import List


class MissingFieldValuesException(Exception):
    def __init__(self, missing_keys: List[str]):
        self.missing_keys = missing_keys

    def __str__(self):
        return f"{self.missing_keys} are required and where not provided in any form (e.g. alias)"
