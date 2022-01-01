import money
from exceptions import *
from tkinter import *
from datetime import datetime
import re
from tkinter import messagebox

window = Tk()
window.geometry("450x340")
window.title("Parkomat")
icon = PhotoImage(file="icon.png")
window.iconphoto(True, icon)


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


def confirm():
    """ Funkcja włączająca się przy zatwiedzeniu przycisku 'Zatwierdź' """

    sum_of_money_label.config(text=moneyHolder.total_amount())


def reset():
    """ Funkcja resetująca parkomat do stanu początkowego """

    moneyHolder.reset()  # reset przechowywacza monet do stanu początkowego tzn. braku monet

    number_of_money_entry.delete(0, "end")  # reset pola z liczbą monet
    number_of_money_entry.insert(0, "1")


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
