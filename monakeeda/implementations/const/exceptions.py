class ConstError(ValueError):
    def __init__(self, value, new_val):
        super(ConstError, self).__init__(
            f'Const field -> its value is {value} ... value given = {new_val}')
