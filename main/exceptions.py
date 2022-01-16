
class IncorrectValueError(Exception):
    """ Wyjątek dla nieprawidłowej wartości wprowadzonej przez użytkownika """
    def __init__(self):
        super().__init__("Invalid value for money")


class TooMuchCoinsError(Exception):
    """ Wyjątek dla monety wrzuconej ponad limit w parkomacie, który wynosi 200 """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class CurrencyMismatchError(Exception):
    """ Wyjątek dla porównywanych pieniędzy, gdy waluty nie są takie same """
    def __init__(self):
        super().__init__("Currencies must match")


class InvalidOperandError(Exception):
    """ Wyjątek dla nieprawidłowej operacji, gdy próbuje się zsumować pieniądz z obiektem niebędącym pieniądzem """
    def __init__(self):
        super().__init__("Invalid operand types for operation")


class UnknownObjectError(Exception):
    """ Wyjątek dla nieznanego obiektu, gdy próbuje się wrzucić coś innego do przechowywacza niż pieniądz """
    def __init__(self):
        super().__init__("Object must be Money")


class IncorrectTime(Exception):
    """ Wyjątek dla nieprawidłowego czasu podanego przez użytkownika """
    def __init__(self):
        super().__init__()
