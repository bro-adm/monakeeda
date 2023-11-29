from collections import defaultdict


class ScopeDict(defaultdict):
    def __init__(self):
        super().__init__(lambda: [], {})


class ScopesDict(defaultdict):
    def __init__(self):
        super().__init__(lambda: ScopeDict(), {})
