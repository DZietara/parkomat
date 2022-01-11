import unittest
from parkomat_functions import ParkomatFunctions
from decimal import Decimal
from datetime import *


class Tests(unittest.TestCase):
    """ Klasa testująca działanie parkomatu """

    parkomat = ParkomatFunctions()

    def test1(self):
        """ Ustaw niepoprawną godzinę. Oczekiwany komunikat o błędzie. Ustawić godzinę na 12:34. """
        self.parkomat.interface.window.hour_entry.delete(0, "end")  # reset entry z godziną
        self.parkomat.interface.window.hour_entry.insert(0, "25")  # wpisanie wartości
        self.parkomat.interface.window.minute_entry.delete(0, "end")  # reset entry z minutą
        self.parkomat.interface.window.minute_entry.insert(0, "61")  # wpisanie wartości
        self.parkomat.change_actual_time("<Button-1>")

        self.parkomat.interface.window.hour_entry.delete(0, "end")  # reset entry z godziną
        self.parkomat.interface.window.hour_entry.insert(0, "12")  # wpisanie wartości
        self.parkomat.interface.window.minute_entry.delete(0, "end")  # reset entry z minutą
        self.parkomat.interface.window.minute_entry.insert(0, "34")  # wpisanie wartości
        self.parkomat.change_actual_time("<Button-1>")
        self.parkomat.reset("<Button-1>")

    def test2(self):
        """ Wrzucić 2zł, oczekiwany termin wyjazdu godzinę po aktualnym czasie. Dorzuć 4zł, oczekiwany termin wyjazdu dwie godziny po aktualnym czasie.
        Dorzuć 5zł, oczekiwany termin wyjazdu trzy godziny po aktualnym czasie. Dorzuć kolejne 5zł, oczekiwany termin wyjazdu cztery godziny po aktualnym czasie."""
        self.parkomat.interface.window.hour_entry.delete(0, "end")  # reset entry z godziną
        self.parkomat.interface.window.hour_entry.insert(0, "12")  # wpisanie wartości
        self.parkomat.interface.window.minute_entry.delete(0, "end")  # reset entry z minutą
        self.parkomat.interface.window.minute_entry.insert(0, "34")  # wpisanie wartości
        self.parkomat.change_actual_time("<Button-1>")

        self.parkomat.add_number_of_money(Decimal("2"))
        self.parkomat.global_date = self.parkomat.global_date + timedelta(hours=1)
        globaldate = self.parkomat.global_date.strftime("%Y-%m-%d %H:%M")
        departuredate = self.parkomat.departure_time.strftime("%Y-%m-%d %H:%M")
        self.assertEqual(globaldate, departuredate)

        self.parkomat.add_number_of_money(Decimal("2"))
        self.parkomat.add_number_of_money(Decimal("2"))
        self.parkomat.global_date = self.parkomat.global_date + timedelta(hours=1)
        globaldate = self.parkomat.global_date.strftime("%Y-%m-%d %H:%M")
        departuredate = self.parkomat.departure_time.strftime("%Y-%m-%d %H:%M")
        self.assertEqual(globaldate, departuredate)

        self.parkomat.add_number_of_money(Decimal("5"))
        self.parkomat.global_date = self.parkomat.global_date + timedelta(hours=1)
        globaldate = self.parkomat.global_date.strftime("%Y-%m-%d %H:%M")
        departuredate = self.parkomat.departure_time.strftime("%Y-%m-%d %H:%M")
        self.assertEqual(globaldate, departuredate)

        self.parkomat.add_number_of_money(Decimal("5"))
        self.parkomat.global_date = self.parkomat.global_date + timedelta(hours=1)
        expected_date = self.parkomat.global_date.strftime("%Y-%m-%d %H:%M")
        departuredate = self.parkomat.departure_time.strftime("%Y-%m-%d %H:%M")
        self.assertEqual(expected_date, departuredate)

        self.parkomat.reset("<Button-1>")

    def test3(self):
        """ Wrzucić tyle pieniędzy, aby termin wyjazdu przeszedł na kolejny dzień,
        zgodnie z zasadami -- wrzucić tyle monet aby termin wyjazdu był po godzinie 19:00, dorzucić monetę 5zł """
        self.parkomat.global_date = self.parkomat.global_date + timedelta(days=1)
        self.parkomat.interface.window.hour_entry.delete(0, "end")  # reset entry z godziną
        self.parkomat.interface.window.hour_entry.insert(0, "19")  # wpisanie wartości
        self.parkomat.interface.window.minute_entry.delete(0, "end")  # reset entry z minutą
        self.parkomat.interface.window.minute_entry.insert(0, "10")  # wpisanie wartości
        self.parkomat.change_actual_time("<Button-1>")
        self.parkomat.add_number_of_money(Decimal("5"))
        self.parkomat.reset("<Button-1>")

    def test4(self):
        """ Wrzucić tyle pieniędzy, aby termin wyjazdu przeszedł na kolejny tydzień, zgodnie z zasadami -
        wrzucić tyle monet aby termin wyjazdu był w piątek po godzinie 19:00, a potem dorzucić monetę 5zł,"""
        self.parkomat.add_number_of_money(Decimal("5"))
        self.parkomat.global_date = datetime.strptime("14 01 2022", '%d %m %Y').replace(hour=19, minute=10)
        self.parkomat.departure_time = datetime.strptime("14 01 2022", '%d %m %Y').replace(hour=19, minute=10)
        self.parkomat.add_number_of_money(Decimal("5"))

        expected_date = datetime.strptime("17-01-2022 08:10", '%d-%m-%Y %H:%M')
        expected_date = expected_date.strftime("%Y-%m-%d %H:%M")

        departure_date = self.parkomat.departure_time.strftime("%Y-%m-%d %H:%M")
        self.assertEqual(expected_date, departure_date)
        self.parkomat.reset("<Button-1>")

    def test5(self):
        """ Wrzucić 1zł, oczekiwany termin wyjazdu pół godziny po aktualnym czasie """
        self.parkomat.interface.window.hour_entry.delete(0, "end")  # reset entry z godziną
        self.parkomat.interface.window.hour_entry.insert(0, "12")  # wpisanie wartości
        self.parkomat.interface.window.minute_entry.delete(0, "end")  # reset entry z minutą
        self.parkomat.interface.window.minute_entry.insert(0, "34")  # wpisanie wartości
        self.parkomat.change_actual_time("<Button-1>")

        self.parkomat.add_number_of_money(Decimal("1"))
        self.parkomat.global_date = self.parkomat.global_date + timedelta(minutes=30)
        expected_date = self.parkomat.global_date.strftime("%Y-%m-%d %H:%M")
        departuredate = self.parkomat.departure_time.strftime("%Y-%m-%d %H:%M")
        self.assertEqual(expected_date, departuredate)
        self.parkomat.reset("<Button-1>")

    def test6(self):
        """ Wrzucić 200 monet 1gr, oczekiwany termin wyjazdu godzinę po aktualnym czasie. """
        self.parkomat.interface.window.hour_entry.delete(0, "end")  # reset entry z godziną
        self.parkomat.interface.window.hour_entry.insert(0, "12")  # wpisanie wartości
        self.parkomat.interface.window.minute_entry.delete(0, "end")  # reset entry z minutą
        self.parkomat.interface.window.minute_entry.insert(0, "34")  # wpisanie wartości
        self.parkomat.change_actual_time("<Button-1>")

        self.parkomat.interface.window.hour_entry.delete(0, "end")  # reset entry z godziną
        self.parkomat.interface.window.hour_entry.insert(0, "12")  # wpisanie wartości
        self.parkomat.interface.window.minute_entry.delete(0, "end")  # reset entry z minutą
        self.parkomat.interface.window.minute_entry.insert(0, "34")  # wpisanie wartości
        self.parkomat.change_actual_time("<Button-1>")
        self.parkomat.interface.window.registration_number_entry.insert(0, "NR123")
        self.parkomat.interface.window.number_of_money_entry.delete(0, "end")
        self.parkomat.interface.window.number_of_money_entry.insert(0, "200")
        self.parkomat.add_number_of_money(Decimal("0.01"))

        self.parkomat.global_date = self.parkomat.global_date + timedelta(hours=1)
        expected_date = self.parkomat.global_date.strftime("%Y-%m-%d %H:%M")
        departuredate = self.parkomat.departure_time.strftime("%Y-%m-%d %H:%M")
        self.assertEqual(expected_date, departuredate)
        self.parkomat.reset("<Button-1>")

    def test7(self):
        """ Wrzucić 201 monet 1gr, oczekiwana informacja o przepełnieniu parkomatu. """
        self.parkomat.interface.window.registration_number_entry.insert(0, "NR123")
        self.parkomat.interface.window.number_of_money_entry.delete(0, "end")
        self.parkomat.interface.window.number_of_money_entry.insert(0, "201")
        self.parkomat.add_number_of_money(Decimal("0.01"))
        self.parkomat.reset("<Button-1>")

    def test8(self):
        """ Wciśnięcie "Zatwierdź" bez wrzucenia monet -- oczekiwana informacja o błędzie. """
        self.parkomat.interface.window.registration_number_entry.insert(0, "NR123")
        self.parkomat.confirm("<Button-1>")
        self.parkomat.reset("<Button-1>")

    def test9(self):
        """Wciśnięcie "Zatwierdź" bez wpisania numeru rejestracyjnego -- oczekiwana informacja o błędzie.
        Wciśnięcie "Zatwierdź" po wpisaniu niepoprawnego numeru rejestracyjnego -- oczekiwana informacja o błędzie."""
        self.parkomat.add_number_of_money(Decimal("5"))
        self.parkomat.confirm("<Button-1>")

        self.parkomat.interface.window.registration_number_entry.insert(0, "asd")
        self.parkomat.confirm("<Button-1>")
        self.parkomat.reset("<Button-1>")


if __name__ == '__main__':
    unittest.main()
