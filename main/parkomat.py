import money
from exceptions import *
from tkinter import *
from datetime import *
from time import *
import re
from tkinter import messagebox

window = Tk()
window.geometry("450x340")
window.title("Parkomat")
icon = PhotoImage(file="icon.png")
window.iconphoto(True, icon)

global_date = datetime.now()  # zmienna globalna przechowująca aktualną datę w parkomacie
h1 = "m"  # zmienna globalna przechowująca wpisaną godzinę
m1 = "h"  # zmienna globalna przechowująca wpisaną minutę


def actual_date():
    """ Funkcja generująca aktualną datę """

    global global_date
    global_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    actual_date_label.config(text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    global_date = datetime.strptime(global_date, "%Y-%m-%d %H:%M:%S")
    actual_date_label.after(1000, actual_date)


def change_actual_time():
    """ Funkcja zmieniająca aktualną datę """

    global global_date
    global h1
    global m1

    temp = global_date.strftime("%Y-%m-%d %H:%M:%S")
    temp = datetime.strptime(temp, "%Y-%m-%d %H:%M:%S") + timedelta(seconds=1)
    global_date = temp
    if hour_entry.get().isdigit() is False or minute_entry.get().isdigit() is False or int(hour_entry.get()) < 0 or int(hour_entry.get()) > 23 or int(minute_entry.get()) < 0 or int(minute_entry.get()) > 59:
        messagebox.showerror("Error", "Wpisz poprawną godzinę.")
    else:
        if hour_entry.get().isdigit():
            if h1 != hour_entry.get():
                h2 = int(hour_entry.get())
                temp = temp.replace(hour=h2)
                h1 = str(h2)
                global_date = temp
        else:
            hour_entry.insert(0, h1)
            messagebox.showerror("Error", "Wpisz poprawną godzinę.")

        if minute_entry.get().isdigit():
            if m1 != minute_entry.get():
                m2 = int(minute_entry.get())
                temp = temp.replace(minute=m2)
                m1 = str(m2)
                global_date = temp
        else:
            minute_entry.insert(0, m1)
            messagebox.showerror("Error", "Wpisz poprawną godzinę.")

        actual_date_label.destroy()
        change_actual_date_button.destroy()

        actual_date_label2.grid(column=1, row=1)
        actual_date_label2.config(text=global_date.strftime("%Y-%m-%d %H:%M:%S"))
        actual_date_label2.after(1000, change_actual_time)


def add_number_of_money(value):
    """ Funkcja dodająca wybraną liczbę monet """

    input_validator()
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


def confirm():
    """ Funkcja włączająca się przy zatwiedzeniu przycisku 'Zatwierdź' """

    if input_validator() is not False:
        sum_of_money_label.config(text=moneyHolder.total_amount())
        confirmation_of_payment()


def reset():
    """ Funkcja resetująca parkomat do stanu początkowego """

    moneyHolder.reset()  # reset przechowywacza monet do stanu początkowego tzn. braku monet

    registration_number_entry.delete(0, "end")  # reset pola z numerem rejestracyjnym

    global global_date
    global_date = datetime.now()

    number_of_money_entry.delete(0, "end")  # reset pola z liczbą monet
    number_of_money_entry.insert(0, "1")


""" Numer rejestracyjny pojazdu """
Label(window, text="Numer rejestracyjny: ", width=20).grid(column=0, row=0)
registration_number_entry = Entry(window, width=20)
registration_number_entry.grid(column=1, row=0)

""" Aktualna data """
Label(window, text="Aktualna data: ", width=20).grid(column=0, row=1)
actual_date_label = Label(window, text="", width=20)
actual_date_label.grid(column=1, row=1)
actual_date()
actual_date_label2 = Label(window, text="", width=20)
""" Pole pozwalające na przestawienie aktualnego czasu """
Label(window, text="Przestaw aktualny czas: ", width=20).grid(column=0, row=2)
""" Godzina """
hour_entry = Entry(window, width=2)
hour_entry.grid(column=1, row=2)
hour_entry.insert(0, "h")
""" Minuta """
minute_entry = Entry(window, width=2)
minute_entry.grid(column=2, row=2)
minute_entry.insert(0, "m")
""" Przycisk przestawiający aktualny czas"""
change_actual_date_button = Button(window, text="Przestaw", width=8, command=lambda: change_actual_time())
change_actual_date_button.grid(column=4, row=2)

""" Data wyjazdu z parkingu """
Label(window, text="Data wyjazdu z parkingu: ", width=20).grid(column=0, row=3)
date_of_departure_label = Label(window, text="", width=20)
date_of_departure_label.grid(column=1, row=3)

""" Uruchomienie funkcji z aktualnym czasem """
actual_date()

""" Liczba wrzucanych monet """
Label(window, text="Liczba wrzuconych monet: ", width=20).grid(column=0, row=4)
number_of_money_entry = Entry(window, width=20)
number_of_money_entry.grid(column=1, row=4)
number_of_money_entry.insert(0, "1")

""" Tworzenie przechowywacza pieniędzy """
moneyHolder = money.MoneyHolder()

""" Pętla tworząca przyciski z pieniędzmi """
i = 6
col = 0
for m in moneyHolder.available_money:
    if i == 12:
        col += 1
        i = 6
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
confirm_button = Button(window, text="Zatwierdź", width=15, pady=12, command=lambda: confirm())
confirm_button.grid(column=0, row=13)
Label(window, text="Suma monet: ", width=20, font="BOLD").grid(column=0, row=14)
sum_of_money_label = Label(window, text="0", width=20)
sum_of_money_label.grid(column=1, row=14)

""" Przycisk resetujący parkomat """
Button(window, text="Reset parkomatu", width=15, pady=12, command=lambda: reset()).grid(column=1, row=13)

window.mainloop()
