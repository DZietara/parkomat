import money
from exceptions import *
from tkinter import *
from datetime import *
import math
import re
from tkinter import messagebox

window = Tk()
window.title("Parkomat")  # tytuł okna programu
icon = PhotoImage(file="icon.png")  #ikona
window.iconphoto(True, icon)  # ustawienie ikony programu

window.resizable(False, False)  # wyłączenie możliwości zmieniania wielkości okna
window_height = 520  # wysokość okna
window_width = 410  # szerokość okna
screen_width = window.winfo_screenwidth()  # szerokość ekranu
screen_height = window.winfo_screenheight()  # wysokość ekranu
x_cordinate = int((screen_width/2) - (window_width/2))  # wyśrodkowanie okna programu w poziomie
y_cordinate = int((screen_height/2) - (window_height/2))  # wyśrodkowanie okna programu w pionie

#  ustawienie rozmiarów wyświetlanego okna programu
window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))


global_date = datetime.now()  # zmienna globalna przechowująca aktualnie ustawioną datę w parkomacie
check = 0  # zmianna globalna przechowująca stan czy przycisk ze zmianą czasu został wciśnięty


def actual_date():
    """ Funkcja generująca aktualną datę """

    global global_date
    global check
    if check == 0:  # jeśli przycisk ze zmianą czasu nie został wciśnięty
        global_date = datetime.now()  # aktualna data
        global_date = global_date.strftime("%Y-%m-%d %H:%M:%S")  # konwertowanie daty na string
        actual_date_label.config(text=global_date)
        global_date = datetime.strptime(global_date, "%Y-%m-%d %H:%M:%S")  # stripowanie daty ze stringa
    else:  #  jeśli przycisk zmianą czasu  został wciśnięty
        global_date = global_date + timedelta(seconds=1)
        global_date = global_date.strftime("%Y-%m-%d %H:%M:%S")
        actual_date_label.config(text=global_date)
        global_date = datetime.strptime(global_date, "%Y-%m-%d %H:%M:%S")

    actual_date_label.after(1000, actual_date)  # powtarzanie funkcji co sekundę z aktualną datą parkomatu


def change_actual_time():
    """ Funkcja ustawiająca godzinę wprowadzoną przez użytkownika """

    global global_date

    #  sprawdzenie czy wpisano poprawnie czas
    if hour_entry.get().isdigit() is False or minute_entry.get().isdigit() is False or int(
            hour_entry.get()) < 0 or int(hour_entry.get()) > 23 or int(minute_entry.get()) < 0 or int(
        minute_entry.get()) > 59:
        messagebox.showerror("Error", "Wpisz poprawną godzinę.")
    else:
        h1 = int(hour_entry.get())  # pobranie godziny z entry i przekonwertowanie na int
        m1 = int(minute_entry.get())  # pobranie minuty z entry i przekonwertowanie na int
        global_date = global_date.replace(hour=h1, minute=m1)  # przypisanie do globalnego czasu zmienionego
        global check
        check = 1  # ustawienie zniennej globalnej na wciśnięty przycisk


def add_number_of_money(value):
    """ Funkcja dodająca wybraną liczbę monet """

    number_of_money = number_of_money_entry.get()  # pobranie liczby monet

    if number_of_money_entry == "" or number_of_money.isdigit() is False:  # jeśli nie wpisano wartości lub nie jest liczbą
        messagebox.showerror("Error", "Wpisz liczbę monet.")  # to wyświetl błąd
    else:  # w przeciwnym wypadku
        number_of_money = int(number_of_money)
        if value < 10:  # jeśli wartość pieniądza wynosi poniżej 10 to tworzymy monetę
            for x in range(number_of_money):  # tworzymy liczbę monet
                try:
                    moneyHolder.add_money(money.Coin(value))
                except TooMuchCoinsError as err:  # przechywcenie wyjątku jeśli spróbowano utworzyć więcej niż 200 razy monetę o jednym nominale
                    messagebox.showerror("Error", err)
                    break
        else:  # w przeciwnym wypadku tworzymy banknoty
            for x in range(number_of_money):  # tworzymy liczbę banknotów
                moneyHolder.add_money(money.Bill(value))
        departure_date()


def input_validator():
    """ Funkcja walidująca numer rejestracyjny """

    pattern = re.match("^[A-Z0-9]+$", registration_number_entry.get())  # porównanie numeru do wyrażenia regularnego
    if registration_number_entry.get() == "":  # błąd jesli nie wpisano numeru rejestracyjnegi
        messagebox.showerror("Error", "Wpisz numer rejestracyjny.")
        return False
    elif bool(pattern) is False:  #  błąd jeśli numer nie pasuje do wyrażenia regularnego
        messagebox.showerror("Error", "Numer rejestracyjny może składać się tylko z wielkich liter od A do Z i cyfr")
        return False


def confirmation_of_payment():
    """ Funkcja wyświetlająca okno z potwierdzeniem zakupu """

    messagebox.showinfo("Potwierdzenie opłacenia parkingu",
                        "Numer rejestracyjny: {} \n\nCzas zakupu: {} \n\nTermin wyjazdu: {}"
                        .format(registration_number_entry.get(), actual_date_label.cget("text"),
                                date_of_departure_label.cget("text")))


def number_of_hours(amount):
    """ Obliczanie ile zostało zapłaconych godzin """
    hours_paid = 0
    if amount == 1:
        hours_paid += 0.5
        amount -= 1
    if amount == 5:
        hours_paid = 1.75
        amount -= 5
    if amount >= 2:
        hours_paid += 1
        amount -= 2
    if amount >= 6:
        hours_paid += 1
        amount -= 4
    if amount >= 11:
        hours_paid += 1
        amount -= 5
    if amount >= 12:
        hp = math.floor((amount / 5))
        hours_paid = hours_paid + hp

    return hours_paid


def departure_date():
    """ Funkcja obliczająca datę wyjazdu """

    global global_date
    actual_time = global_date  # aktualny czas parkomatu
    amount = moneyHolder.total_amount()  # suma przechowywanych pieniędzy
    hours_paid = number_of_hours(amount)  # liczba zapłaconych godzin

    """strefa od poniedziałku do piątku: 8-20"""

    for x in range(hours_paid):
        temp = actual_time + timedelta(hours=hours_paid)
        if temp.weekday() not in [5, 6]:
            departure_time = actual_time + timedelta(hours=hours_paid)
        # elif temp.weekday() == 5: #DOKOŃCZYĆ

    departure_time = actual_time + timedelta(hours=hours_paid)
    date_of_departure_label.config(text=departure_time.strftime("%Y-%m-%d %H:%M:%S"))


def confirm():
    """ Funkcja włączająca się przy zatwiedzeniu przycisku 'Zatwierdź' """

    if input_validator() is not False:  # sprawdzenie walidacji numeru rejestracyjnego
        if moneyHolder.total_amount() > 0:  # wykonanie jeśli suma monet jest większa od 0
            sum_of_money_label.config(text=moneyHolder.total_amount())
            confirmation_of_payment()  # wykonanie funkcji potwierdzającej płatność
        else:  # w przeciwnym wypadku wyświetl błąd
            messagebox.showerror("Error", "Nie wrzucono monet.")


def reset():
    """ Funkcja resetująca parkomat do stanu początkowego """

    moneyHolder.reset()  # reset przechowywacza monet do stanu początkowego tzn. braku monet

    registration_number_entry.delete(0, "end")  # reset pola z numerem rejestracyjnym
    sum_of_money_label.config(text="0")  # reset pola z sumą monet
    date_of_departure_label.config(text="")  # reset pola z datą wyjazdu

    global global_date
    global_date = datetime.now()  # reset czasu parkomatu do stanu początkowego

    number_of_money_entry.delete(0, "end")  # reset pola z liczbą monet
    number_of_money_entry.insert(0, "1")  # wpisanie domyślnej wartości
    hour_entry.delete(0, "end")  # reset entry z godziną
    hour_entry.insert(0, "0")  # wpisanie domyślnej wartości
    minute_entry.delete(0, "end")  # reset entry z minutą
    minute_entry.insert(0, "0")  # wpisanie domyślnej wartości


""" Numer rejestracyjny pojazdu """
Label(window, text="Numer rejestracyjny: ", width=20, pady=15).grid(column=0, row=0)
registration_number_entry = Entry(window, width=20)
registration_number_entry.grid(column=1, row=0)

""" Aktualna data """
Label(window, text="Aktualna data: ", width=20).grid(column=0, row=1)
actual_date_label = Label(window, text="", width=20)
actual_date_label.grid(column=1, row=1)
""" Uruchomienie funkcji z aktualnym czasem """
actual_date()
""" Pole pozwalające na przestawienie aktualnego czasu """
Label(window, text="Przestaw aktualny czas: ", width=20).grid(column=0, row=2)
""" Godzina """
Label(window, text="wprowadź godzinę ", width=20).grid(column=1, row=2)
hour_entry = Entry(window, width=2)
hour_entry.grid(column=2, row=2)
hour_entry.insert(0, "0")
""" Minuta """
Label(window, text="wprowadź minutę", width=20).grid(column=1, row=3)
minute_entry = Entry(window, width=2)
minute_entry.grid(column=2, row=3)
minute_entry.insert(0, "0")
""" Przycisk przestawiający aktualny czas"""
change_actual_date_button = Button(window, text="Przestaw", width=8, command=lambda: change_actual_time())
change_actual_date_button.grid(column=1, row=4)

""" Data wyjazdu z parkingu """
Label(window, text="Data wyjazdu z parkingu: ", width=20, pady=15).grid(column=0, row=6)
date_of_departure_label = Label(window, text="", width=20)
date_of_departure_label.grid(column=1, row=6)

""" Liczba wrzucanych monet """
Label(window, text="Liczba wrzuconych monet: ", width=20).grid(column=0, row=7)
number_of_money_entry = Entry(window, width=20)
number_of_money_entry.grid(column=1, row=7)
number_of_money_entry.insert(0, "1")
Label(window, width=20).grid(row=8)

""" Tworzenie przechowywacza pieniędzy """
moneyHolder = money.MoneyHolder()

""" Pętla tworząca przyciski z pieniędzmi """
i = 9  # zmienna przechowująca aktualny rząd
col = 0  # zmienna przechowująca aktualna kolumnę
for m in moneyHolder.available_money:
    if i == 15:  # jeśli utworzono 6 monet to tworzenie przycisków w następnej kolumnie i ustawienie wartość rzędu na początkową
        col += 1
        i = 9
    if m < 10:  # jeśli moneta tworzymy przecisk z monetą
        button1 = Button(window, text=str(m) + " " + moneyHolder.currency, width=15,
                         command=lambda m=m: add_number_of_money(m))
        button1.grid(column=col, row=i)
        i += 1
    else:  # w przeciwnym wypadku tworzymy przycisk z banknotem
        button2 = Button(window, text=str(m) + " " + moneyHolder.currency, width=15,
                         command=lambda m=m: add_number_of_money(m))
        button2.grid(column=col, row=i)
        i += 1

""" Przycisk Zatwierdź """
Label(window, width=20).grid(row=16)
confirm_button = Button(window, text="Zatwierdź", width=42, pady=3, command=lambda: confirm())
confirm_button.grid(column=0, row=17, columnspan=2)

""" Przycisk Reset """
reset_button = Button(window, text="Reset parkomatu", width=42, pady=3, command=lambda: reset())
reset_button.grid(column=0, row=18, columnspan=2, pady=3)

""" Pole pokazujące sumę wrzuconych monet """
Label(window, text="Suma monet: ", width=20, font="BOLD", pady=15).grid(column=0, row=20)
sum_of_money_label = Label(window, text="0", width=20, font="BOLD")
sum_of_money_label.grid(column=1, row=20)

window.mainloop()
