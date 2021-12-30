"""Wyjątki dla operacji związanych z pieniędzmi"""


class InvalidValueError(Exception):
    def __init__(self):
        super().__init__("Invalid value money")


class CurrencyMismatchError(Exception):
    def __init__(self):
        super().__init__("Currencies must match")


class InvalidOperandError(Exception):
    def __init__(self):
        super().__init__("Invalid operand types for operation")


class UnknownObjectError(Exception):
    def __init__(self):
        super().__init__("Object must be Money")
