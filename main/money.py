from exceptions import *
from decimal import Decimal


class Money:
    """Klasa reprezentująca pieniądz"""

    def __init__(self, value, currency="PLN"):
        self.__value = round(Decimal(value), 2)
        self.__currency = currency

    @property
    def value(self):
        """Zwraca wartość pieniądza"""
        return self.__value

    @property
    def currency(self):
        """Zwraca walutę pieniądza"""
        return self.__currency

    def __add__(self, other):
        if not isinstance(other, Money):
            raise InvalidOperandError

        if self.currency != other.currency:
            raise CurrencyMismatchError
        return self.value + other.value

    def __sub__(self, other):
        if not isinstance(other, Money):
            raise InvalidOperandError

        if self.currency != other.currency:
            raise CurrencyMismatchError
        return self.value - other.value

    def __repr__(self):
        return 'Money({}, "{}")'.format(self.value, self.currency)


class Coin(Money):
    """Klasa reprezentująca monetę"""

    __available_coins = [Decimal("0.01"),
                         Decimal("0.02"),
                         Decimal("0.05"),
                         Decimal("0.10"),
                         Decimal("0.20"),
                         Decimal("0.50"),
                         Decimal("1"),
                         Decimal("2"),
                         Decimal("5")]

    def __init__(self, value, currency="PLN"):
        if round(Decimal(value), 2) in self.__available_coins:
            if currency.upper() != "PLN":
                raise WrongCurrencyError
            else:
                super().__init__(value, currency)
        else:
            raise InvalidValueError

    def __repr__(self):
        return 'Coin({}, "{}")'.format(self.value, self.currency)


class Bill(Money):
    """Klasa reprezentująca banknot"""

    __available_bills = [Decimal("10"),
                         Decimal("20"),
                         Decimal("50")]

    def __init__(self, value, currency="PLN"):
        if round(Decimal(value), 2) in self.__available_bills:
            if currency.upper() != "PLN":
                raise WrongCurrencyError
            else:
                super().__init__(value, currency)
        else:
            raise InvalidValueError

    def __repr__(self):
        return 'Bill({}, "{}")'.format(self.value, self.currency)
