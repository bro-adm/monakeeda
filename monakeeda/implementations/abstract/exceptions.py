class AbstractFieldFoundError(ValueError):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f"Abstract field not implemented"
