class AbstractFieldFoundError(ValueError):
    def __init__(self, key):
        self.key = key

    def __str__(self):
        return f"Abstract field {self.key} not implemented"
