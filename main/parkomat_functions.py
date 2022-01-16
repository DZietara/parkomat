import money
from exceptions import *
from tkinter import *
from datetime import *
from decimal import Decimal
import math
import re
from tkinter import messagebox
from dateutil.rrule import *
from parkomat_interface import ParkomatInterface


class ParkomatFunctions:
    """ Klasa realizująca funkcjonalności programu """

    __global_date = datetime.now()  # zmienna przechowująca aktualnie ustawioną datę w parkomacie
    __departure_time = __global_date  # zmienna przechowująca czas wyjazdu
    __previous_time = 0  # zmienna przechowująca poprzednio zwrócony czas w sekundach dla wrzuconych pieniędzy dla metody seconds_for_money
    __inserted_money_by_user = Decimal("0.00")  # zmienna przechowująca liczbę wrzuconych pieniędzy przez aktualnego użytkownika

    def __init__(self):
        self.__window = Tk()  # Toplevel widget reprezentujący główne okno programu
        self.__interface = ParkomatInterface(self.window)  # interfejs programu
        self.__moneyHolder = self.interface.moneyHolder  # instancja przechowywacza pieniędzy
        self.buttons_onclick()  # metoda dodające wydarzenia do przycisków
        self.actual_date()  # metoda aktualizująca datę parkomatu oraz wyjazdu

    @property
    def window(self):
        """ Getter zwracający Toplevel widget reprezentujący główne okno programu """
        return self.__window

    @window.setter
    def window(self, window):
        """ Setter ustawiający Toplevel widget reprezentujący główne okno programu """
        self.__window = window

    @property
    def interface(self):
        """ Getter zwracający odwołanie do interfejsu programu """
        return self.__interface

    @interface.setter
    def interface(self, interface):
        """ Setter ustawiające odwołanie do interfejsu programu """
        self.__interface = interface

    @property
    def moneyHolder(self):
        """ Getter zwracający przechowywacz pieniędzy """
        return self.__moneyHolder

    @moneyHolder.setter
    def moneyHolder(self, moneyHolder):
        """ Setter ustawiający przechowywacz pieniędzy """
        self.__moneyHolder = moneyHolder

    @property
    def global_date(self):
        """ Getter zwracający aktualnie ustawioną datę w parkomacie """
        return self.__global_date

    @property
    def departure_time(self):
        """ Getter zwracający datę wyjazdu """
        return self.__departure_time

    @global_date.setter
    def global_date(self, global_date):
        """ Setter ustawiający aktualną datę w parkomacie """
        self.__global_date = global_date

    @departure_time.setter
    def departure_time(self, departure_time):
        """ Setter ustawiający datę wyjazdu  """
        self.__departure_time = departure_time

    @property
    def previous_time(self):
        """ Getter zwracający poprzednio dodany czas """
        return self.__previous_time

    @previous_time.setter
    def previous_time(self, previous_time):
        """ SSetter ustawiający poprzednio dodany czas """
        self.__previous_time = previous_time

    @property
    def inserted_money_by_user(self):
        """ Getter zwracający poprzednio dodany czas """
        return self.__inserted_money_by_user

    @inserted_money_by_user.setter
    def inserted_money_by_user(self, inserted_money_by_user):
        """ SSetter ustawiający poprzednio dodany czas """
        self.__inserted_money_by_user = inserted_money_by_user

    def main_loop(self):
        """ Nieskończona pętla służąca do uruchomienia aplikacji trwająca, dopóki okno nie zostanie zamknięte """
        self.window.mainloop()

    def buttons_onclick(self):
        """ Metoda obsługująca wydarzenia, gdy przycisk zostanie wciśnięty """

        self.interface.window.button1.bind("<ButtonRelease-1>", lambda event: self.add_number_of_money(self.moneyHolder.available_values[0]))
        self.interface.window.button2.bind("<ButtonRelease-1>", lambda event: self.add_number_of_money(self.moneyHolder.available_values[1]))
        self.interface.window.button3.bind("<ButtonRelease-1>", lambda event: self.add_number_of_money(self.moneyHolder.available_values[2]))
        self.interface.window.button4.bind("<ButtonRelease-1>", lambda event: self.add_number_of_money(self.moneyHolder.available_values[3]))
        self.interface.window.button5.bind("<ButtonRelease-1>", lambda event: self.add_number_of_money(self.moneyHolder.available_values[4]))
        self.interface.window.button6.bind("<ButtonRelease-1>", lambda event: self.add_number_of_money(self.moneyHolder.available_values[5]))
        self.interface.window.button7.bind("<ButtonRelease-1>", lambda event: self.add_number_of_money(self.moneyHolder.available_values[6]))
        self.interface.window.button8.bind("<ButtonRelease-1>", lambda event: self.add_number_of_money(self.moneyHolder.available_values[7]))
        self.interface.window.button9.bind("<ButtonRelease-1>", lambda event: self.add_number_of_money(self.moneyHolder.available_values[8]))
        self.interface.window.button10.bind("<ButtonRelease-1>", lambda event: self.add_number_of_money(self.moneyHolder.available_values[9]))
        self.interface.window.button11.bind("<ButtonRelease-1>", lambda event: self.add_number_of_money(self.moneyHolder.available_values[10]))
        self.interface.window.button12.bind("<ButtonRelease-1>", lambda event: self.add_number_of_money(self.moneyHolder.available_values[11]))
        self.bind_button_confirm(lambda event: self.button_confirm(event))
        self.bind_change_actual_time(lambda event: self.button_change_actual_time(event))

    def actual_date(self):
        """ Metoda aktualizująca aktualną datę parkomatu oraz datę wyjazdu"""

        self.global_date = self.global_date + timedelta(seconds=1)  # dodanie sekundy do aktualnej daty parkomatu
        self.departure_time = self.departure_time + timedelta(seconds=1)  # dodanie sekundy do daty wyjazdu

        # wyświetlenie aktualnej daty parkomatu
        self.interface.window.actual_date_label.config(text=self.global_date.strftime("%Y-%m-%d %H:%M"))
        # wyświetlenie daty wyjazdu
        self.interface.window.date_of_departure_label.config(text=self.departure_time.strftime("%Y-%m-%d %H:%M"))

        # powtarzanie funkcji actual_date() co sekundę
        self.interface.window.actual_date_label.after(1000, self.actual_date)

    def button_confirm(self, event):
        """ Funkcja odpowiadająca na naciśnięcie przycisku 'Zatwierdź' """
        try:
            self.confirm()
        except Exception as err:
            messagebox.showerror("Błąd", str(err))

    def button_change_actual_time(self, event):
        """ Funkcja odpowiadająca na naciśnięcie przycisku zmieniającego godzinę """
        try:
            self.change_actual_time()
        except Exception as err:
            messagebox.showerror("Błąd", str(err))

    def bind_button_confirm(self, f):
        """ Funkcja bindująca przycisk 'Zatwierdź' """
        self.interface.window.confirm_button.bind("<ButtonRelease-1>", f)

    def bind_change_actual_time(self, f):
        """ Funkcja bindująca przycisk 'Przestaw' """
        self.interface.window.change_actual_date_button.bind("<ButtonRelease-1>", f)

    def change_actual_time(self):
        """ Metoda ustawiająca godzinę wprowadzoną przez użytkownika """

        #  sprawdzenie, czy wpisano poprawnie czas
        if self.inserted_money_by_user != Decimal("0.00"):
            messagebox.showerror("Error", "Nie można zmienić czasu, gdy wrzucono już pieniądze.")
        else:
            if self.interface.window.hour_entry.get().isdigit() is False or self.interface.window.minute_entry.get().isdigit() is False or int(
                    self.interface.window.hour_entry.get()) < 0 or int(
                self.interface.window.hour_entry.get()) > 23 or int(
                self.interface.window.minute_entry.get()) < 0 or int(
                self.interface.window.minute_entry.get()) > 59:
                raise IncorrectTime("Wpisano niepoprawny czas.")
            else:
                h1 = int(self.interface.window.hour_entry.get())  # pobranie godziny z entry i przekonwertowanie na int
                m1 = int(self.interface.window.minute_entry.get())  # pobranie minuty z entry i przekonwertowanie na int
                self.global_date = self.global_date.replace(hour=h1, minute=m1)  # ustawienie nowego czasy dla parkomatu
                self.departure_time = self.global_date  # przypisanie aktualnej daty parkomatu do daty wyjazdu
                self.previous_time = 0  # reset wcześniejszego czasu, gdy zmieniamy czas

    def add_number_of_money(self, value: Decimal):
        """ Metoda dodająca wybraną liczbę monet """

        number_of_money = self.interface.window.number_of_money_entry.get()  # pobranie wprowadzonej liczby monet
        try:
            if self.interface.window.number_of_money_entry == "" or number_of_money.isdigit() is False:  # jeśli nie wpisano wartości lub nie jest liczbą
                raise IncorrectValueError
            else:  # w przeciwnym wypadku
                number_of_money = int(number_of_money)
                if value < 10:  # jeśli wartość pieniądza wynosi poniżej 10 to tworzymy monetę
                    for x in range(number_of_money):
                        self.moneyHolder.add_money(money.Coin(value))  # dodanie monety do przechowywacza
                        self.inserted_money_by_user += value  # dodanie wartości monety do aktualnie wrzuconych przez użytkownika
                else:  # w przeciwnym wypadku tworzymy banknoty
                    for x in range(number_of_money):
                        self.moneyHolder.add_money(money.Bill(value))  # dodanie banknotu do przechowywacza
                        self.inserted_money_by_user += value  # dodanie wartości banknotu do aktualnie wrzuconych przez użytkownika
        except IncorrectValueError:  # przechwycenie wyjątku dla niepoprawnie wpisanej wartości
            messagebox.showerror("Error", "Wpisz poprawną liczbę pieniędzy którą chcesz wrzucić.")
        except TooMuchCoinsError as err:  # przechwycenie wyjątku, jeśli przekroczono limit nominałów
            messagebox.showerror("Error", str(err))
        finally:  # aktualizacja wrzuconej kwoty oraz daty wyjazdu
            self.interface.window.sum_of_money_label.config(text=self.inserted_money_by_user)  # wrzucona kwota
            self.departure_date()  # aktualizacja daty wyjazdu

    def input_validator(self):
        """ Metoda walidująca numer rejestracyjny """

        # porównanie numeru do wyrażenia regularnego
        pattern = re.match("^[A-Z0-9]+$", self.interface.window.registration_number_entry.get())
        if self.interface.window.registration_number_entry.get() == "":  # błąd jeśli nie wpisano numeru rejestracyjnego
            raise RegistrationNumberError("Wpisz numer rejestracyjny.")
        elif bool(pattern) is False:  # błąd, jeśli numer nie pasuje do wyrażenia regularnego
            raise RegistrationNumberError("Numer rejestracyjny może składać się tylko z wielkich liter od A do Z i cyfr")

    def confirmation_of_payment(self):
        """ Metoda wyświetlająca okno z potwierdzeniem opłacenia parkingu """

        messagebox.showinfo("Potwierdzenie opłacenia parkingu",
                            "Numer rejestracyjny: {} \n\nCzas zakupu: {} \n\nTermin wyjazdu: {}"
                            .format(self.interface.window.registration_number_entry.get(),
                                    self.interface.window.actual_date_label.cget("text"),
                                    self.interface.window.date_of_departure_label.cget("text")))

    def rules(self, departure_date, seconds):
        """ Zasady strefy płatnego parkowania obowiązuje w godzinach od 8 do 20 od poniedziałku do piątku """

        rr = rrule(SECONDLY, byweekday=(MO, TU, WE, TH, FR), byhour=(8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19),
                   dtstart=departure_date, interval=seconds)
        return rr.after(departure_date)

    def seconds_for_money(self, amount: Decimal):
        """ Metoda zwracająca liczbę sekund dla wrzuconych pieniędzy """

        total_seconds = 0  # zmienna przechowująca sumę dodanych sekund
        grosz_1h = 60 * 60 / 200  # sekunda za jednego grosza pierwszej godziny
        grosz_2h = 60 * 60 / 400  # sekunda za jednego grosza drugiej godziny
        grosz_xh = 60 * 60 / 500  # sekunda za jednego grosza lub większej godziny

        if total_seconds < 3600:  # jeśli suma sekund jest mniejsza od godziny zapisanej w sekundach
            if amount >= 2:  # jeśli suma jest większa lub równa 2
                total_seconds += 3600  # dodaj godzinę
                amount -= 2  # odejmij od sumy koszt jednej godziny
            else:
                seconds = amount * 100 * Decimal(grosz_1h)  # obliczona liczba sekund
                total_seconds += seconds  # dodanie obliczonych sekund do całościowej liczby sekund
                amount = 0  # zerowanie sumy

        if total_seconds < 7200:  # jeśli suma sekund jest mniejsza od dwóch godzin zapisanej w sekundach
            if amount >= 4:  # jeśli suma jest większa lub równa 4
                total_seconds += 3600  # dodaj godzinę
                amount -= 4  # odejmij od sumy koszt jednej godziny
            else:
                seconds = amount * 100 * Decimal(grosz_2h)  # obliczona liczba sekund
                total_seconds += seconds  # dodanie obliczonych sekund do całościowej liczby sekund
                amount = 0  # zerowanie sumy

        while amount > 0:  # wykonuj, dopóki suma wrzuconych pieniędzy jest większa od zera
            if total_seconds >= 7200:  # jeśli suma sekund jest większa lub równa dwóch godzin zapisanej w sekundach
                if amount >= 5:  # jeśli suma jest większa lub równa 5
                    total_seconds += math.floor((amount / 5)) * 60 * 60  # dodanie całkowitej liczby godzin
                    amount -= 5 * math.floor((amount / 5))  # odjęcia całkowitej liczby godzin od sumy
                else:
                    seconds = amount * 100 * Decimal(grosz_xh)  # obliczona liczba sekund
                    total_seconds += seconds  # dodanie obliczonych sekund do całościowej liczby sekund
                    amount = 0  # zerowanie sumy

        temp_seconds = total_seconds
        total_seconds -= self.previous_time  # od całkowitego czasu odjęcie wcześniejszego
        self.previous_time = temp_seconds  # ustawienie nowego wcześniejszego czasu

        return int(total_seconds)

    def departure_date(self):
        """ Metoda ustawiająca datę wyjazdu """

        free_hours = [x for x in range(0, 24) if x not in range(8, 20)]  # lista z darmowymi godzinami
        amount = self.inserted_money_by_user  # suma przechowywanych pieniędzy
        seconds_paid = self.seconds_for_money(amount)  # liczba zapłaconych sekund
        if seconds_paid > 0:  # jeśli liczba zapłaconych sekund jest większa od zera
            if self.departure_time.weekday() == 5:  # jeśli jest sobota
                self.departure_time = self.departure_time.replace(hour=8, minute=00) + timedelta(days=2)

            elif self.departure_time.weekday() == 6:  # jeśli jest niedziela
                self.departure_time = self.departure_time.replace(hour=8, minute=00) + timedelta(days=1)

            elif self.departure_time.hour in free_hours:  # jeśli są dni robocze i aktualna godzina jest darmowa
                if self.departure_time.hour > 19:  # jeśli jest po godzinie 19:00
                    self.departure_time = self.departure_time.replace(hour=8, minute=00) + timedelta(days=1)
                else:  # jeśli jest godzina między 0 a 8
                    self.departure_time = self.departure_time.replace(hour=8, minute=00)

            # wyświetlenie w label zaktualizowanej daty wyjazdu
            self.departure_time = self.rules(self.departure_time, seconds_paid)
            self.interface.window.date_of_departure_label.config(text=self.departure_time.strftime("%Y-%m-%d %H:%M"))

    def confirm(self):
        """ Funkcja włączająca się przy kliknięciu przycisku 'Zatwierdź' """

        self.input_validator()  # sprawdzenie walidacji numeru rejestracyjnego
        if self.inserted_money_by_user > 0:  # wykonanie, jeśli suma monet jest większa od 0
            self.confirmation_of_payment()  # wykonanie funkcji potwierdzającej płatność
            self.reset()  # po potwierdzeniu rezerwacji reset parkomatu do stanu początkowego
        else:  # w przeciwnym wypadku wyświetl błąd
            raise NotInsertedMoney("Nie wrzucono pieniędzy.")

    def reset(self):
        """ Funkcja resetująca parkomat do stanu początkowego """

        self.interface.window.registration_number_entry.delete(0, "end")  # reset pola z numerem rejestracyjnym
        self.interface.window.sum_of_money_label.config(text="0.00")  # reset pola z wrzuconymi pieniędzmi
        self.interface.window.date_of_departure_label.config(text="")  # reset pola z datą wyjazdu
        self.global_date = datetime.now()  # reset czasu parkomatu do stanu początkowego
        self.departure_time = self.global_date  # ustawienie z powrotem czasu wyjazdy do stanu początkowego
        self.interface.window.number_of_money_entry.delete(0, "end")  # reset pola z liczbą monet
        self.interface.window.number_of_money_entry.insert(0, "1")  # wpisanie domyślnej wartości
        self.interface.window.hour_entry.delete(0, "end")  # reset entry z godziną
        self.interface.window.hour_entry.insert(0, "0")  # wpisanie domyślnej wartości
        self.interface.window.minute_entry.delete(0, "end")  # reset entry z minutą
        self.interface.window.minute_entry.insert(0, "0")  # wpisanie domyślnej wartości
        self.previous_time = 0  # reset poprzednio dodanego czasu
        self.inserted_money_by_user = Decimal("0.00")  # reset wrzuconych pieniędzy dla użytkownika
