from collections import defaultdict
from functools import reduce


class ExceptionsDict(defaultdict):
    def __init__(self):
        super().__init__(lambda: [], {})

    def __bool__(self):
        for key, exceptions in self.items():
            if exceptions:
                return True

        return False

    def __str__(self):
        final_str = ""

        for key, exceptions in self.items():
            if exceptions:
                exceptions_str = str(reduce(lambda x1, x2: f"{x1} \n\t * {x2}", exceptions))
                final_str += f" \n {key} -> \n\t * {exceptions_str}"

        return final_str
