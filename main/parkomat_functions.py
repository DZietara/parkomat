import money
from exceptions import *
from tkinter import *
from datetime import *
import math
import re
from tkinter import messagebox
from dateutil.rrule import *
from parkomat_interface import ParkomatInterface


class ParkomatFunctions:
    """ Klasa realizująca funkcjonalności programu """

    __global_date = datetime.now()  # zmienna przechowująca aktualnie ustawioną datę w parkomacie
    __check = 0  # zmienna przechowująca stan czy przycisk ze zmianą czasu został wciśnięty
    __departure_time = __global_date  # zmienna przechowująca czas wyjazdu
    __hours_bought = 0  # zmienna przechowująca aktualnie wykupioną liczbę godzin
    __sum_of_money_used = 0  # zmienna przechowująca sumę użytych pieniędzy to wykupienia godzin

    def __init__(self):
        self.__window = Tk()
        self.__interface = ParkomatInterface(self.window)
        self.__moneyHolder = self.interface.moneyHolder
        self.buttons_onclick()
        self.actual_date()

    def main_loop(self):
        self.window.mainloop()

    @property
    def window(self):
        return self.__window

    @window.setter
    def window(self, window):
        self.__window = window

    @property
    def interface(self):
        return self.__interface

    @interface.setter
    def interface(self, interface):
        self.__interface = interface

    @property
    def moneyHolder(self):
        return self.__moneyHolder

    @moneyHolder.setter
    def moneyHolder(self, moneyHolder):
        self.__moneyHolder = moneyHolder

    @property
    def global_date(self):
        """ Getter zwracający aktualnie ustawioną datę w parkomacie """
        return self.__global_date

    @property
    def check(self):
        """ Getter zwracający stan czy przycisk ze zmianą czasu został wciśnięty """
        return self.__check

    @property
    def departure_time (self):
        """ Getter zwracający datę wyjazdu """
        return self.__departure_time

    @property
    def hours_bought(self):
        """ Getter zwracający liczbę kupionych godzin """
        return self.__hours_bought

    @property
    def sum_of_money_used(self):
        """ Getter zwracający sumę użytych pieniędzy na kupno godzin """
        return self.__sum_of_money_used

    @global_date.setter
    def global_date(self, global_date):
        """ Setter ustawiający aktualną datę w parkomacie """
        self.__global_date = global_date

    @check.setter
    def check(self, check):
        """ Setter ustawiający stan czy przycisk ze zmianą czasu został wciśnięty """
        self.__check = check

    @departure_time.setter
    def departure_time(self, departure_time):
        """ Setter ustawiający datę wyjazdu  """
        self.__departure_time = departure_time

    @hours_bought.setter
    def hours_bought(self, hours_bought):
        """ Setter ustawiający liczbę kupionych godzin """
        self.__hours_bought = hours_bought

    @sum_of_money_used.setter
    def sum_of_money_used(self, sum_of_money_used):
        """ Setter ustawiający sumę użytych pieniędzy na kupno godzin """
        self.__sum_of_money_used = sum_of_money_used

    def buttons_onclick(self):
        """ Metoda obsługująca wydarzenie, gdy przycisk zostanie wciśnięty """

        self.interface.window.button1.bind("<Button-1>", lambda event: self.add_number_of_money(self.moneyHolder.available_money[0]))
        self.interface.window.button2.bind("<Button-1>", lambda event: self.add_number_of_money(self.moneyHolder.available_money[1]))
        self.interface.window.button3.bind("<Button-1>", lambda event: self.add_number_of_money(self.moneyHolder.available_money[2]))
        self.interface.window.button4.bind("<Button-1>", lambda event: self.add_number_of_money(self.moneyHolder.available_money[3]))
        self.interface.window.button5.bind("<Button-1>", lambda event: self.add_number_of_money(self.moneyHolder.available_money[4]))
        self.interface.window.button6.bind("<Button-1>>", lambda event: self.add_number_of_money(self.moneyHolder.available_money[5]))
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
        """ Metoda generująca aktualną datę """

        if self.check == 0:  # jeśli przycisk ze zmianą czasu nie został wciśnięty
            self.global_date = datetime.now()  # aktualna data
            self.global_date = self.global_date.strftime("%Y-%m-%d %H:%M:%S")  # konwertowanie daty na string
            self.interface.window.actual_date_label.config(text=self.global_date)
            self.global_date = datetime.strptime(self.global_date, "%Y-%m-%d %H:%M:%S")  # stripowanie daty ze stringa
        else:  # jeśli przycisk zmianą czasu został wciśnięty
            self.global_date = self.global_date + timedelta(seconds=1)
            self.global_date = self.global_date.strftime("%Y-%m-%d %H:%M:%S")
            self.interface.window.actual_date_label.config(text=self.global_date)
            self.global_date = datetime.strptime(self.global_date, "%Y-%m-%d %H:%M:%S")

        # powtarzanie funkcji co sekundę z aktualną datą parkomatu
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
            self.global_date = self.global_date.replace(hour=h1, minute=m1)  # przypisanie do globalnego czasu zmienionego
            self.check = 1  # ustawienie zniennej globalnej na wciśnięty przycisk
            self.departure_time = self.global_date
            self.departure_time = self.departure_time + timedelta(seconds=1)
            self.interface.window.date_of_departure_label.config(text=self.departure_time)

    def add_number_of_money(self, value):
        """ Metoda dodająca wybraną liczbę monet """

        number_of_money = self.interface.window.number_of_money_entry.get()  # pobranie liczby monet

        if self.interface.window.number_of_money_entry == "" or number_of_money.isdigit() is False:  # jeśli nie wpisano wartości lub nie jest liczbą
            messagebox.showerror("Error", "Wpisz liczbę monet.")  # to wyświetl błąd
        else:  # w przeciwnym wypadku
            number_of_money = int(number_of_money)
            if value < 10:  # jeśli wartość pieniądza wynosi poniżej 10 to tworzymy monetę
                for x in range(number_of_money):  # tworzymy liczbę monet
                    try:
                        self.moneyHolder.add_money(money.Coin(value))
                    except TooMuchCoinsError as err:  # przechywcenie wyjątku jeśli spróbowano utworzyć więcej niż 200 razy monetę o jednym nominale
                        messagebox.showerror("Error", str(err))
                        break
            else:  # w przeciwnym wypadku tworzymy banknoty
                for x in range(number_of_money):  # tworzymy liczbę banknotów
                    self.moneyHolder.add_money(money.Bill(value))
            self.interface.window.sum_of_money_label.config(text=self.moneyHolder.total_amount())
            self.departure_date()

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

    def rules(self, start, x):
        """ Zasady strefy płatnego parkowania obowiązuje w godzinach od 8 do 20 od poniedziałku do piątku """

        rr = rrule(SECONDLY, byweekday=(MO, TU, WE, TH, FR), byhour=(8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19),
                   dtstart=start, interval=x)
        return rr.after(start)

    def number_of_hours(self, amount):
        """ Metoda obliczająca ile zostało zapłaconych godzin """

        hours_paid = 0  # zmienna przechowująca
        amount = amount - self.sum_of_money_used

        if amount == 1 and self.hours_bought < 1:
            hours_paid += 0.5
            amount -= 1
            self.sum_of_money_used += 1
            self.hours_bought += 0.5
        if amount == 5 and self.hours_bought == 0:
            hours_paid += 1.75
            amount -= 5
            self.sum_of_money_used += 5
            self.hours_bought = 2
        if amount >= 2 and self.hours_bought == 0:
            hours_paid += 1
            amount -= 2
            self.sum_of_money_used += 2
            self.hours_bought = 1
        if amount >= 4 and 0.5 <= self.hours_bought <= 1:
            hours_paid += 1
            amount -= 4
            self.sum_of_money_used += 4
            self.hours_bought = 2
        if amount >= 5 and self.hours_bought == 2:
            hours_paid = hours_paid + math.floor((amount / 5))
            self.hours_bought = 2
            self.sum_of_money_used += (5 * math.floor((amount / 5)))
            amount -= (5 * hours_paid)

        return hours_paid

    def departure_date(self):
        """ Metoda ustawiająca datę wyjazdu """

        hour_free = [0, 1, 2, 3, 4, 5, 6, 7, 20, 21, 22, 23]
        amount = self.moneyHolder.total_amount()  # suma przechowywanych pieniędzy
        hours_paid = self.number_of_hours(amount) * 60 * 60  # liczba zapłaconych godzin zmieniona na sekundy
        if hours_paid > 0:
            if self.departure_time.hour in hour_free:
                if hours_paid == 3600*1.75:
                    if self.departure_time.hour > 19:
                        self.departure_time = self.departure_time.replace(hour=9, minute=45) + timedelta(days=1)
                    else:
                        self.departure_time = self.departure_time.replace(hour=9, minute=45)
                    self.interface.window.date_of_departure_label.config(text=self.departure_time.strftime("%Y-%m-%d %H:%M:%S"))
                elif hours_paid == 3600:
                    if self.departure_time.hour > 19:
                        self.departure_time = self.departure_time.replace(hour=9, minute=0) + timedelta(days=1)
                    else:
                        self.departure_time = self.departure_time.replace(hour=9, minute=0)
                    self.interface.window.date_of_departure_label.config(text=self.departure_time.strftime("%Y-%m-%d %H:%M:%S"))
                elif hours_paid == 1800:
                    if self.departure_time.hour > 19:
                        self.departure_time = self.departure_time.replace(hour=8, minute=30) + timedelta(days=1)
                    else:
                        self.departure_time = self.departure_time.replace(hour=8, minute=30)
                    self.interface.window.date_of_departure_label.config(text=self.departure_time.strftime("%Y-%m-%d %H:%M:%S"))
                elif hours_paid >= 3600*1.75:
                    if self.departure_time.hour > 19:
                        self.departure_time = self.departure_time.replace(hour=8, minute=0) + timedelta(days=1)
                    else:
                        self.departure_time = self.departure_time.replace(hour=8, minute=0)
                    self.departure_time = self.rules(self.departure_time, int(hours_paid))
                    self.interface.window.date_of_departure_label.config(text=self.departure_time.strftime("%Y-%m-%d %H:%M:%S"))
            else:
                self.departure_time = self.rules(self.departure_time, int(hours_paid))
                self.interface.window.date_of_departure_label.config(text=self.departure_time.strftime("%Y-%m-%d %H:%M:%S"))

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
        self.hours_bought = 0  # reset liczby godzin zamówiona w parkomacie do stanu początkowego
        self.sum_of_money_used = 0  # reset sumy użytych pieniędzy do opłacenia do stanu początkowego
        self.interface.window.number_of_money_entry.delete(0, "end")  # reset pola z liczbą monet
        self.interface.window.number_of_money_entry.insert(0, "1")  # wpisanie domyślnej wartości
        self.interface.window.hour_entry.delete(0, "end")  # reset entry z godziną
        self.interface.window.hour_entry.insert(0, "0")  # wpisanie domyślnej wartości
        self.interface.window.minute_entry.delete(0, "end")  # reset entry z minutą
        self.interface.window.minute_entry.insert(0, "0")  # wpisanie domyślnej wartości

