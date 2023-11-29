class MissingFieldValueException(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return f"Field required and was not provided in any form (e.g. alias)"
