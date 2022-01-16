import unittest
from parkomat_functions import ParkomatFunctions
from decimal import Decimal
from datetime import *
from exceptions import *


class Tests(unittest.TestCase):
    """ Klasa testująca działanie parkomatu """

    parkomat = ParkomatFunctions()

    def test1(self):
        """ Ustaw niepoprawną godzinę. Oczekiwany komunikat o błędzie. Ustawić godzinę na 12:34. """

        # sprawdzamy, czy wystąpił wyjątek dla nieprawidłowego czasu podanego przez użytkownika
        with self.assertRaises(IncorrectTime):
            self.parkomat.interface.window.hour_entry.delete(0, "end")  # reset entry z godziną
            self.parkomat.interface.window.hour_entry.insert(0, "25")  # wpisanie niepoprawnej wartości
            self.parkomat.interface.window.minute_entry.delete(0, "end")  # reset entry z minutą
            self.parkomat.interface.window.minute_entry.insert(0, "15")  # wpisanie poprawnej wartości
            self.parkomat.change_actual_time()

        # ustawiamy poprawną godzinę 12:34
        self.parkomat.interface.window.hour_entry.delete(0, "end")  # reset entry z godziną
        self.parkomat.interface.window.hour_entry.insert(0, "12")  # wpisanie poprawnej wartości
        self.parkomat.interface.window.minute_entry.delete(0, "end")  # reset entry z minutą
        self.parkomat.interface.window.minute_entry.insert(0, "34")  # wpisanie poprawnej wartości
        self.parkomat.change_actual_time()  # przycisk ustawiający godzinę

        global_date = self.parkomat.global_date.strftime("%H:%M")
        self.assertEqual("12:34", global_date)  # oczekiwana ustawiona godzina na 12:34

    def test2(self):
        """ Wrzucić 2zł, oczekiwany termin wyjazdu godzinę po aktualnym czasie. Dorzuć 4zł, oczekiwany termin wyjazdu dwie godziny po aktualnym czasie.
        Dorzuć 5zł, oczekiwany termin wyjazdu trzy godziny po aktualnym czasie. Dorzuć kolejne 5zł, oczekiwany termin wyjazdu cztery godziny po aktualnym czasie."""
        self.parkomat.global_date = datetime.strptime("17-01-2022 08:10", "%d-%m-%Y %H:%M")  # aktualny czas
        self.parkomat.departure_time = datetime.strptime("17-01-2022 08:10", "%d-%m-%Y %H:%M")

        self.parkomat.add_number_of_money(Decimal("2"))  # wrzucamy 2zł
        departure_date = self.parkomat.departure_time.strftime("%d-%m-%Y %H:%M")
        self.assertEqual("17-01-2022 09:10", departure_date)  # oczekiwany termin wyjazdu godzinę po aktualnym czasie

        self.parkomat.add_number_of_money(Decimal("2"))  # wrzucamy 4zł
        self.parkomat.add_number_of_money(Decimal("2"))
        departure_date = self.parkomat.departure_time.strftime("%d-%m-%Y %H:%M")
        self.assertEqual("17-01-2022 10:10", departure_date)  # oczekiwany termin wyjazdu dwie godziny po aktualnym czasie

        self.parkomat.add_number_of_money(Decimal("5"))  # wrzucamy 5zł
        departure_date = self.parkomat.departure_time.strftime("%d-%m-%Y %H:%M")
        self.assertEqual("17-01-2022 11:10", departure_date)  # oczekiwany termin wyjazdu trzy godziny po aktualnym czasie

        self.parkomat.add_number_of_money(Decimal("5"))  # wrzucamy kolejne 5zł
        departure_date = self.parkomat.departure_time.strftime("%d-%m-%Y %H:%M")
        self.assertEqual("17-01-2022 12:10", departure_date)  # oczekiwany termin wyjazdu cztery godziny po aktualnym czasie

        self.parkomat.reset()  # reset parkomatu

    def test3(self):
        """ Wrzucić tyle pieniędzy, aby termin wyjazdu przeszedł na kolejny dzień,
        zgodnie z zasadami -- wrzucić tyle monet aby termin wyjazdu był po godzinie 19:00, dorzucić monetę 5zł """
        self.parkomat.add_number_of_money(Decimal("5"))  # wrzucamy tyle pieniędzy, aby termin wyjazdu przeszedł na kolejny dzień
        self.parkomat.add_number_of_money(Decimal("5"))
        self.parkomat.add_number_of_money(Decimal("5"))
        self.parkomat.departure_time = datetime.strptime("17-01-2022 19:10", "%d-%m-%Y %H:%M")  # termin wyjazdu po godzinie 19:00

        self.parkomat.add_number_of_money(Decimal("5"))  # dorzucamy monetę 5zł
        departure_date = self.parkomat.departure_time.strftime("%d-%m-%Y %H:%M")

        self.assertEqual("18-01-2022 08:10", departure_date)  # oczekiwany termin wyjazdu następny dzień 08:10
        self.parkomat.reset()  # reset parkomatu

    def test4(self):
        """ Wrzucić tyle pieniędzy, aby termin wyjazdu przeszedł na kolejny tydzień, zgodnie z zasadami -
        wrzucić tyle monet aby termin wyjazdu był w piątek po godzinie 19:00, a potem dorzucić monetę 5zł,"""
        self.parkomat.add_number_of_money(Decimal("5"))  # wrzucamy tyle pieniędzy, aby termin wyjazdu przeszedł na kolejny tydzień
        self.parkomat.add_number_of_money(Decimal("5"))
        self.parkomat.add_number_of_money(Decimal("5"))
        self.parkomat.departure_time = datetime.strptime("14-01-2022 19:10", "%d-%m-%Y %H:%M")  # termin wyjazdu piątek po godzinie 19:00

        self.parkomat.add_number_of_money(Decimal("5"))  # dorzucamy monetę 5zł
        departure_date = self.parkomat.departure_time.strftime("%d-%m-%Y %H:%M")

        self.assertEqual("17-01-2022 08:10", departure_date)  # oczekiwany termin wyjazdu następny możliwy dzień tzn. poniedziałek 08:10
        self.parkomat.reset()  # reset parkomatu

    def test5(self):
        """ Wrzucić 1zł, oczekiwany termin wyjazdu pół godziny po aktualnym czasie """
        self.parkomat.departure_time = datetime.strptime("17-01-2022 08:10", "%d-%m-%Y %H:%M")

        self.parkomat.add_number_of_money(Decimal("1"))  # dorzucamy monetę 1zł
        departure_date = self.parkomat.departure_time.strftime("%d-%m-%Y %H:%M")

        self.assertEqual("17-01-2022 08:40", departure_date)  # oczekiwany termin wyjazdu pół godziny po aktualnym czasie
        self.parkomat.reset()  # reset parkomatu

    def test6(self):
        """ Wrzucić 200 monet 1gr, oczekiwany termin wyjazdu godzinę po aktualnym czasie. """
        self.parkomat.global_date = datetime.strptime("17-01-2022 08:10", '%d-%m-%Y %H:%M')
        self.parkomat.departure_time = datetime.strptime("17-01-2022 08:10", '%d-%m-%Y %H:%M')

        self.parkomat.interface.window.registration_number_entry.insert(0, "NR123")
        self.parkomat.interface.window.number_of_money_entry.delete(0, "end")
        self.parkomat.interface.window.number_of_money_entry.insert(0, "200")
        self.parkomat.add_number_of_money(Decimal("0.01"))

        departure_date = self.parkomat.departure_time.strftime("%d-%m-%Y %H:%M")
        self.assertEqual("17-01-2022 09:10", departure_date)
        self.parkomat.reset()  # reset parkomatu

    def test7(self):
        """ Wrzucić 201 monet 1gr, oczekiwana informacja o przepełnieniu parkomatu. """
        self.parkomat.interface.window.registration_number_entry.insert(0, "NR123")  # ustawienie nr rejestracyjnego
        self.parkomat.interface.window.number_of_money_entry.delete(0, "end")

        self.parkomat.interface.window.number_of_money_entry.insert(0, "201")
        self.parkomat.add_number_of_money(Decimal("0.01"))  # oczekiwana informacja o przepełnieniu parkomatu
        self.assertEqual(Decimal("2.00"), self.parkomat.moneyHolder.total_amount())

        self.parkomat.reset()  # reset parkomatu

    def test8(self):
        """ Wciśnięcie "Zatwierdź" bez wrzucenia monet -- oczekiwana informacja o błędzie. """

        # sprawdzamy, czy wystąpił wyjątek, gdy użytkownik nie wrzucił pieniędzy i wcisnął przycisk 'Zatwierdź'
        with self.assertRaises(NotInsertedMoney):
            self.parkomat.interface.window.registration_number_entry.insert(0, "NR123")  # ustawienie nr rejestracyjnego
            self.parkomat.confirm()  # wciśnięcie "Zatwierdź" bez wrzucenia monet, oczekiwana informacja o błędzie

        self.parkomat.reset()  # reset parkomatu

    def test9(self):
        """Wciśnięcie "Zatwierdź" bez wpisania numeru rejestracyjnego -- oczekiwana informacja o błędzie.
        Wciśnięcie "Zatwierdź" po wpisaniu niepoprawnego numeru rejestracyjnego -- oczekiwana informacja o błędzie."""

        # wciśnięcie "Zatwierdź" bez wpisania numeru rejestracyjnego, oczekiwana informacja o błędzie
        with self.assertRaises(RegistrationNumberError):
            self.parkomat.add_number_of_money(Decimal("5"))  # wrzucamy 5zl
            self.parkomat.confirm()

        # wciśnięcie "Zatwierdź" po wpisaniu niepoprawnego numeru rejestracyjnego -- oczekiwana informacja o błędzie
        with self.assertRaises(RegistrationNumberError):
            self.parkomat.add_number_of_money(Decimal("5"))  # wrzucamy 5zl
            self.parkomat.interface.window.registration_number_entry.insert(0, "asd")   # niepoprawny numer rejestracyjny
            self.parkomat.confirm()

        self.parkomat.reset()  # reset parkomatu


if __name__ == '__main__':
    unittest.main()
