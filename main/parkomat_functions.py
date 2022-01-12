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
    __previous_time = 0  # zmienna przechowująca poprzednio dodany czas w sekundach

    def __init__(self):
        self.__window = Tk()  # Toplevel widget reprezentujący główne okno programu
        self.__interface = ParkomatInterface(self.window)  # interfejs programu
        self.__moneyHolder = self.interface.moneyHolder  # instancja przechowywacza pieniędzy
        self.buttons_onclick()  # metoda dodające wydarzenia do przycisków
        self.actual_date()  # metoda aktualizująca datę parkomatu oraz wyjazdu

    def main_loop(self):
        """ Nieskończona pętla służąca do uruchomienia aplikacji trwająca dopóki okno nie zostanie zamknięte """
        self.window.mainloop()

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

    def buttons_onclick(self):
        """ Metoda obsługująca wydarzenie, gdy przycisk zostanie wciśnięty """

        self.interface.window.button1.bind("<Button-1>", lambda event: self.add_number_of_money(self.moneyHolder.available_money[0]))
        self.interface.window.button2.bind("<Button-1>", lambda event: self.add_number_of_money(self.moneyHolder.available_money[1]))
        self.interface.window.button3.bind("<Button-1>", lambda event: self.add_number_of_money(self.moneyHolder.available_money[2]))
        self.interface.window.button4.bind("<Button-1>", lambda event: self.add_number_of_money(self.moneyHolder.available_money[3]))
        self.interface.window.button5.bind("<Button-1>", lambda event: self.add_number_of_money(self.moneyHolder.available_money[4]))
        self.interface.window.button6.bind("<Button-1>", lambda event: self.add_number_of_money(self.moneyHolder.available_money[5]))
        self.interface.window.button7.bind("<Button-1>", lambda event: self.add_number_of_money(self.moneyHolder.available_money[6]))
        self.interface.window.button8.bind("<Button-1>", lambda event: self.add_number_of_money(self.moneyHolder.available_money[7]))
        self.interface.window.button9.bind("<Button-1>", lambda event: self.add_number_of_money(self.moneyHolder.available_money[8]))
        self.interface.window.button10.bind("<Button-1>", lambda event: self.add_number_of_money(self.moneyHolder.available_money[9]))
        self.interface.window.button11.bind("<Button-1>", lambda event: self.add_number_of_money(self.moneyHolder.available_money[10]))
        self.interface.window.button12.bind("<Button-1>", lambda event: self.add_number_of_money(self.moneyHolder.available_money[11]))
        self.interface.window.confirm_button.bind("<Button-1>", lambda event: self.confirm(event))
        self.interface.window.reset_button.bind("<Button-1>", lambda event: self.reset(event))
        self.interface.window.change_actual_date_button.bind("<Button-1>", lambda event: self.change_actual_time(event))

    def actual_date(self):
        """ Metoda generująca aktualną datę parkomatu oraz daty wyjazdu"""

        self.global_date = self.global_date + timedelta(seconds=1)  # dodanie sekundy do aktualnej daty parkomatu
        self.departure_time = self.departure_time + timedelta(seconds=1)  # dodanie sekundy do daty wyjazdu

        # wyświetlenie aktualnej daty parkomatu
        self.interface.window.actual_date_label.config(text=self.global_date.strftime("%Y-%m-%d %H:%M"))
        # wyświetlenie daty wyjazdu
        self.interface.window.date_of_departure_label.config(text=self.departure_time.strftime("%Y-%m-%d %H:%M"))

        # powtarzanie funkcji actual_date() co sekundę
        self.interface.window.actual_date_label.after(1000, self.actual_date)

    def change_actual_time(self, event):
        """ Metoda ustawiająca godzinę wprowadzoną przez użytkownika """

        #  sprawdzenie, czy wpisano poprawnie czas
        if self.interface.window.hour_entry.get().isdigit() is False or self.interface.window.minute_entry.get().isdigit() is False or int(
                self.interface.window.hour_entry.get()) < 0 or int(self.interface.window.hour_entry.get()) > 23 or int(self.interface.window.minute_entry.get()) < 0 or int(
            self.interface.window.minute_entry.get()) > 59:
            messagebox.showerror("Error", "Wpisz poprawną godzinę.")
        else:
            h1 = int(self.interface.window.hour_entry.get())  # pobranie godziny z entry i przekonwertowanie na int
            m1 = int(self.interface.window.minute_entry.get())  # pobranie minuty z entry i przekonwertowanie na int
            self.global_date = self.global_date.replace(hour=h1, minute=m1)  # ustawienie nowego czasy dla parkomatu
            self.departure_time = self.global_date  # przypisanie aktualnej daty parkomatu do daty wyjazdu
            self.moneyHolder.reset()  # reset przechowywacza gdy zmieniamy czas
            self.previous_time = 0  # reset wcześniejszego czasu gdy zmieniamy czas

    def add_number_of_money(self, value):
        """ Metoda dodająca wybraną liczbę monet """

        number_of_money = self.interface.window.number_of_money_entry.get()  # pobranie wprowadzonej liczby monet

        if self.interface.window.number_of_money_entry == "" or number_of_money.isdigit() is False:  # jeśli nie wpisano wartości lub nie jest liczbą
            messagebox.showerror("Error", "Wpisz liczbę monet.")  # to wyświetl błąd
        else:  # w przeciwnym wypadku
            number_of_money = int(number_of_money)
            if value < 10:  # jeśli wartość pieniądza wynosi poniżej 10 to tworzymy monetę
                for x in range(number_of_money):  # tworzenie podanej liczby monet
                    try:
                        self.moneyHolder.add_money(money.Coin(value))
                    except TooMuchCoinsError as err:  # przechywcenie wyjątku jeśli spróbowano utworzyć więcej niż 200 razy monetę o jednym nominale
                        messagebox.showerror("Error", str(err))
                        break
            else:  # w przeciwnym wypadku tworzymy banknoty
                for x in range(number_of_money):  # tworzenie podanej liczby banknotów
                    self.moneyHolder.add_money(money.Bill(value))
            self.interface.window.sum_of_money_label.config(text=self.moneyHolder.total_amount())  # wpisanie sumy pieniędzy do pola
            self.departure_date()  # aktualizacja daty wyjazdu

    def input_validator(self):
        """ Metoda walidująca numer rejestracyjny """

        pattern = re.match("^[A-Z0-9]+$", self.interface.window.registration_number_entry.get())  # porównanie numeru do wyrażenia regularnego
        if self.interface.window.registration_number_entry.get() == "":  # błąd jesli nie wpisano numeru rejestracyjnegi
            messagebox.showerror("Error", "Wpisz numer rejestracyjny.")
            return False
        elif bool(pattern) is False:  # błąd jeśli numer nie pasuje do wyrażenia regularnego
            messagebox.showerror("Error",
                                 "Numer rejestracyjny może składać się tylko z wielkich liter od A do Z i cyfr")
            return False

    def confirmation_of_payment(self):
        """ Metoda wyświetlająca okno z potwierdzeniem zakupu """

        messagebox.showinfo("Potwierdzenie opłacenia parkingu",
                            "Numer rejestracyjny: {} \n\nCzas zakupu: {} \n\nTermin wyjazdu: {}"
                            .format(self.interface.window.registration_number_entry.get(), self.interface.window.actual_date_label.cget("text"),
                                    self.interface.window.date_of_departure_label.cget("text")))

    def rules(self, start, seconds):
        """ Zasady strefy płatnego parkowania obowiązuje w godzinach od 8 do 20 od poniedziałku do piątku """

        rr = rrule(SECONDLY, byweekday=(MO, TU, WE, TH, FR), byhour=(8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19),
                   dtstart=start, interval=seconds)
        return rr.after(start)

    def seconds_for_money(self, amount):
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

        hour_free = [0, 1, 2, 3, 4, 5, 6, 7, 20, 21, 22, 23]  # lista z darmowymi godzinami
        amount = self.moneyHolder.total_amount()  # suma przechowywanych pieniędzy
        seconds_paid = self.seconds_for_money(amount)  # liczba zapłaconych sekund
        if seconds_paid > 0:
            if self.departure_time.hour in hour_free:  # jeśli aktualna godzina wyjazdu jest darmowa
                if self.departure_time.hour > 19:  # jeśli aktualna godzina wyjazdu jest między 19-24
                    self.departure_time = self.departure_time.replace(hour=8, minute=00) + timedelta(days=1, seconds=seconds_paid)
                else:
                    self.departure_time = self.departure_time.replace(hour=8, minute=00) + timedelta(seconds=seconds_paid)
                self.interface.window.date_of_departure_label.config(text=self.departure_time.strftime("%Y-%m-%d %H:%M"))
            elif self.departure_time.hour == 19 and seconds_paid == 6300:
                self.departure_time = self.departure_time.replace(hour=8, minute=45)
                self.interface.window.date_of_departure_label.config(text=self.departure_time.strftime("%Y-%m-%d %H:%M"))
            else:  # jeśli aktualna godzina wyjazdu nie jest darmowa
                self.departure_time = self.rules(self.departure_time, seconds_paid)
                self.interface.window.date_of_departure_label.config(text=self.departure_time.strftime("%Y-%m-%d %H:%M"))

    def confirm(self, event):
        """ Funkcja włączająca się przy zatwiedzeniu przycisku 'Zatwierdź' """

        if self.input_validator() is not False:  # sprawdzenie walidacji numeru rejestracyjnego
            if self.moneyHolder.total_amount() > 0:  # wykonanie jeśli suma monet jest większa od 0
                self.interface.window.sum_of_money_label.config(text=self.moneyHolder.total_amount())
                self.confirmation_of_payment()  # wykonanie funkcji potwierdzającej płatność
                self.reset(event)  # po potwierdzeniu rezerwacji reset parkomatu do stanu początkowego
            else:  # w przeciwnym wypadku wyświetl błąd
                messagebox.showerror("Error", "Nie wrzucono monet.")

    def reset(self, event):
        """ Funkcja resetująca parkomat do stanu początkowego """

        self.moneyHolder.reset()  # reset przechowywacza monet do stanu początkowego tzn. braku monet
        self.interface.window.registration_number_entry.delete(0, "end")  # reset pola z numerem rejestracyjnym
        self.interface.window.sum_of_money_label.config(text="0")  # reset pola z sumą monet
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


