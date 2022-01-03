import money
from exceptions import *
from tkinter import *
from datetime import *
from time import *
import math
import re
from tkinter import messagebox

window = Tk()
window.geometry("410x520")
window.title("Parkomat")
icon = PhotoImage(file="icon.png")
window.iconphoto(True, icon)

global_date = datetime.now()  # zmienna globalna przechowująca aktualną datę w parkomacie
check = 0  # sprawdzenie czy przycisk ze zmianą czasu został wciśnięty


def actual_date():
    """ Funkcja generująca aktualną datę """

    global global_date
    global check
    if check == 0:
        global_date = datetime.now()
        global_date = global_date.strftime("%Y-%m-%d %H:%M:%S")
        actual_date_label.config(text=global_date)
        global_date = datetime.strptime(global_date, "%Y-%m-%d %H:%M:%S")
    else:
        global_date = global_date + timedelta(seconds=1)
        global_date = global_date.strftime("%Y-%m-%d %H:%M:%S")
        actual_date_label.config(text=global_date)
        global_date = datetime.strptime(global_date, "%Y-%m-%d %H:%M:%S")

    actual_date_label.after(1000, actual_date)


def change_actual_time():
    """ Funkcja ustawiająca godzinę wprowadzoną przez użytkownika """

    global global_date
    if hour_entry.get().isdigit() is False or minute_entry.get().isdigit() is False or int(
            hour_entry.get()) < 0 or int(hour_entry.get()) > 23 or int(minute_entry.get()) < 0 or int(
        minute_entry.get()) > 59:
        messagebox.showerror("Error", "Wpisz poprawną godzinę.")
    else:
        h1 = int(hour_entry.get())
        m1 = int(minute_entry.get())
        temp = global_date.replace(hour=h1)
        temp = temp.replace(minute=m1)
        global_date = temp
        global check
        check = 1


def add_number_of_money(value):
    """ Funkcja dodająca wybraną liczbę monet """

    number_of_money = number_of_money_entry.get()

    if number_of_money_entry == "" or number_of_money.isdigit() is False:
        messagebox.showerror("Error", "Wpisz liczbę monet.")
    else:
        number_of_money = int(number_of_money)
        if value < 10:
            for x in range(number_of_money):
                try:
                    moneyHolder.add_money(money.Coin(value))
                except TooMuchCoinsError as err:
                    messagebox.showerror("Error", err)
                    break
        else:
            for x in range(number_of_money):
                moneyHolder.add_money(money.Bill(value))
        departure_date()


def input_validator():
    """ Funkcja walidująca numer rejestracyjny """

    pattern = re.match("^[A-Z0-9]+$", registration_number_entry.get())
    if registration_number_entry.get() == "":
        messagebox.showerror("Error", "Wpisz numer rejestracyjny.")
        return False
    elif bool(pattern) is False:
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
    actual_time = global_date
    amount = moneyHolder.total_amount()
    hours_paid = number_of_hours(amount)

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

    if input_validator() is not False:
        if moneyHolder.total_amount() > 0:
            sum_of_money_label.config(text=moneyHolder.total_amount())
            confirmation_of_payment()
        else:
            messagebox.showerror("Error", "Nie wrzucono monet.")


def reset():
    """ Funkcja resetująca parkomat do stanu początkowego """

    moneyHolder.reset()  # reset przechowywacza monet do stanu początkowego tzn. braku monet

    registration_number_entry.delete(0, "end")  # reset pola z numerem rejestracyjnym
    sum_of_money_label.config(text="0")  #
    date_of_departure_label.config(text="")
    global global_date
    global_date = datetime.now()

    number_of_money_entry.delete(0, "end")  # reset pola z liczbą monet
    number_of_money_entry.insert(0, "1")


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
i = 9
col = 0
for m in moneyHolder.available_money:
    if i == 15:
        col += 1
        i = 9
    if m < 10:
        button1 = Button(window, text=str(m) + " " + moneyHolder.currency, width=15,
                         command=lambda m=m: add_number_of_money(m))
        button1.grid(column=col, row=i)
        i += 1
    else:
        button2 = Button(window, text=str(m) + " " + moneyHolder.currency, width=15,
                         command=lambda m=m: add_number_of_money(m))
        button2.grid(column=col, row=i)
        i += 1

""" Przycisk Zatwierdź """
Label(window, width=20).grid(row=16)
confirm_button = Button(window, text="Zatwierdź", width=42, pady=3, command=lambda: confirm())
confirm_button.grid(column=0, row=17, columnspan=2)

""" Przycisk resetujący parkomat """
reset_button = Button(window, text="Reset parkomatu", width=42, pady=3, command=lambda: reset())
reset_button.grid(column=0, row=18, columnspan=2, pady=3)

""" Pole pokazujące sumę wrzuconych monet """
Label(window, text="Suma monet: ", width=20, font="BOLD", pady=15).grid(column=0, row=20)
sum_of_money_label = Label(window, text="0", width=20, font="BOLD")
sum_of_money_label.grid(column=1, row=20)

window.mainloop()
