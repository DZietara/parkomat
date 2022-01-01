"""Wyjątki dla operacji związanych z pieniędzmi"""


class IncorrectValueError(Exception):
    def __init__(self):
        super().__init__("Invalid value for money")


class TooMuchCoinsError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class CurrencyMismatchError(Exception):
    def __init__(self):
        super().__init__("Currencies must match")


class InvalidOperandError(Exception):
    def __init__(self):
        super().__init__("Invalid operand types for operation")


class UnknownObjectError(Exception):
    def __init__(self):
        super().__init__("Object must be Money")
