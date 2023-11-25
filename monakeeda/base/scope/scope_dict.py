from collections import defaultdict


class ScopeDict(defaultdict):
    """
    key = label
    value = list of components
    """

    def __init__(self):
        super().__init__(lambda: [], {})
