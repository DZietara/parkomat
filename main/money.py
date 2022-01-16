from exceptions import *
from decimal import Decimal


class Money:
    """ Klasa reprezentująca pieniądz """

    def __init__(self, value, currency="PLN"):
        self.__value = round(Decimal(value), 2)  # konwertowanie wpisanej wartości na Decimal i zaokrąglenie do 2 miejsc
        self.__currency = currency.upper()  # zmienienie wpisanej waluty na wielkie litery

    @property
    def value(self):
        """ Getter zwracający wartość pieniądza """
        return self.__value

    @property
    def currency(self):
        """ Getter zwracający walutę pieniądza """
        return self.__currency

    def __add__(self, other):
        """ Funkcja zwracająca wartość dodanych do siebie pieniędzy """
        if not isinstance(other, Money):
            raise InvalidOperandError

        if self.currency != other.currency:
            raise CurrencyMismatchError
        return self.value + other.value

    def __sub__(self, other):
        """ Funkcja zwracająca wartość odjętych od siebie pieniędzy """
        if not isinstance(other, Money):
            raise InvalidOperandError

        if self.currency != other.currency:
            raise CurrencyMismatchError
        return self.value - other.value

    def __repr__(self):
        return 'Money({}, "{}")'.format(self.value, self.currency)


class Coin(Money):
    """ Klasa reprezentująca monetę """

    __available_values = [Decimal("0.01"),
                          Decimal("0.02"),
                          Decimal("0.05"),
                          Decimal("0.10"),
                          Decimal("0.20"),
                          Decimal("0.50"),
                          Decimal("1"),
                          Decimal("2"),
                          Decimal("5")]

    def __init__(self, value, currency="PLN"):
        if round(Decimal(value), 2) in self.available_values:  # sprawdzenie czy jest możliwe stworzenie monety o podanym nominale
            super().__init__(value, currency)  # wywołanie konstruktora z klasy nadrzędnej
        else:
            raise IncorrectValueError()  # error jeśli podany nominał nie znajduje się na liście

    def __repr__(self):
        return 'Coin({}, "{}")'.format(self.value, self.currency)

    @property
    def available_values(self):
        """ Getter zwracający listę możliwych nominałów monet do stworzenia """
        return self.__available_values


class Bill(Money):
    """ Klasa reprezentująca banknot """

    __available_values = [Decimal("10"),
                          Decimal("20"),
                          Decimal("50")]

    def __init__(self, value, currency="PLN"):
        if round(Decimal(value),2) in self.available_values:  # sprawdzenie czy jest możliwe stworzenie bankontu o podanym nominale
            super().__init__(value, currency)  # wywołanie konstruktora z klasy nadrzędnej
        else:
            raise IncorrectValueError()  # error jeśli podany nominał nie znajduje się na liście

    def __repr__(self):
        return 'Bill({}, "{}")'.format(self.value, self.currency)

    @property
    def available_values(self):
        """ Getter zwracający listę możliwych nominałów banknotów do stworzenia """
        return self.__available_values


class MoneyHolder:
    """ Klasa reprezentująca przechowywacz pieniędzy """

    __list_of_money = []
    __currency = "PLN"
    __available_values = [Decimal("0.01"),
                          Decimal("0.02"),
                          Decimal("0.05"),
                          Decimal("0.10"),
                          Decimal("0.20"),
                          Decimal("0.50"),
                          Decimal("1"),
                          Decimal("2"),
                          Decimal("5"),
                          Decimal("10"),
                          Decimal("20"),
                          Decimal("50")]

    def __init__(self, currency="PLN"):
        self.__currency = currency.upper()

    def __repr__(self):
        return 'MoneyHolder({})'.format(self.list_of_money)

    @property
    def currency(self):
        """ Getter zwracający walutę obsługiwaną w przechowywaczu """
        return self.__currency

    @property
    def available_values(self):
        """ Getter zwracający listę możliwych nominałów pieniędzy w przechowywaczu """
        return self.__available_values

    @property
    def list_of_money(self):
        """ Zwrócenie listy wrzuconych pieniędzy """
        return self.__list_of_money

    def add_money(self, money):
        """ Metoda dodająca pieniądz do przechowywacza """

        if isinstance(money, Money):
            if money.currency == self.currency:
                if isinstance(money, Bill):
                    self.list_of_money.append(money)
                if isinstance(money, Coin):
                    if self.number_of_coins(money) < 200:
                        self.list_of_money.append(money)
                    else:
                        raise TooMuchCoinsError(
                            "Parkomat przepełniony monetami o nominale {} {}, wrzuć pieniądz o innym nominale.".format(
                                money.value, money.currency))
            else:
                raise CurrencyMismatchError
        else:
            raise UnknownObjectError

    def total_amount(self):
        """ Metoda zwracająca sumę wartości pieniędzy znajdujących się w przechowywaczu """
        return sum([money.value for money in self.list_of_money])

    def number_of_coins(self, money):
        """ Metoda zwracająca liczbę monet danego rodzaju """
        return len([coin.value for coin in self.list_of_money if coin.value == money.value])

    def reset(self):
        """ Metoda resetująca listę monet """
        self.list_of_money.clear()
