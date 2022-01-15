
class IncorrectValueError(Exception):
    """ Wyjątek gdy wprowadzono nieprawidłową wartość """
    def __init__(self):
        super().__init__()


class TooMuchCoinsError(Exception):
    """ Wyjątek gdy do parkomatu próbuje się wrzucić monetę z nominałem ponad limit """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class CurrencyMismatchError(Exception):
    """ Wyjątek gdy waluty nie są takie same """
    def __init__(self):
        super().__init__("Currencies must match")


class InvalidOperandError(Exception):
    """ Wyjątek gdy zła operacja dla konkretnego typu """
    def __init__(self):
        super().__init__("Invalid operand types for operation")


class UnknownObjectError(Exception):
    """ Wyjątek gdy jest zła operacja dla konkretnego typu """
    def __init__(self):
        super().__init__("Object must be Money")


class IncorrectTime(Exception):
    """ Wyjątek dla nieprawidłowego czasu """
    def __init__(self):
        super().__init__()
