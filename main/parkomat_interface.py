from tkinter import *
import money


class ParkomatInterface:
    """ Klasa tworząca interfejs użytkownika """

    def __init__(self, root):
        self.__window = root
        self.window_settings()
        self.__moneyHolder = money.MoneyHolder()
        self.init_ui()

    @property
    def window(self):
        """ Getter zwracający Toplevel widget reprezentujący główne okno programu """
        return self.__window

    @window.setter
    def window(self, window):
        """ Setter ustawiający Toplevel widget reprezentujący główne okno programu """
        self.__window = window

    @property
    def moneyHolder(self):
        """ Getter zwracający przechowywacz pieniędzy """
        return self.__moneyHolder

    @moneyHolder.setter
    def moneyHolder(self, moneyHolder):
        """ Setter ustawiający przechowywacz pieniędzy """
        self.__moneyHolder = moneyHolder

    def window_settings(self):
        """ Metoda zmieniająca ustawienia okna programu """

        self.window.title("Parkomat")  # tytuł okna programu
        self.window.icon = PhotoImage(file="icon.png")  # ikona
        self.window.iconphoto(True, self.window.icon)  # ustawienie ikony programu
        self.window.resizable(False, False)  # wyłączenie możliwości zmiany rozmiaru okna
        self.window.window_height = 500  # wysokość okna
        self.window.window_width = 410  # szerokość okna
        self.window.screen_width = self.window.winfo_screenwidth()  # szerokość ekranu
        self.window.screen_height = self.window.winfo_screenheight()  # wysokość ekranu

        # wyśrodkowanie okna programu w poziomie
        self.window.x_cordinate = int((self.window.screen_width / 2) - (self.window.window_width / 2))
        # wyśrodkowanie okna programu w pionie
        self.window.y_cordinate = int((self.window.screen_height / 2) - (self.window.window_height / 2))

        # ustawienie rozmiarów wyświetlanego okna programu
        self.window.geometry("{}x{}+{}+{}".format(self.window.window_width, self.window.window_height, self.window.x_cordinate, self.window.y_cordinate))

    def money_buttons(self):
        """ Metoda tworząca przyciski z pieniędzmi """

        self.window.button1 = Button(self.window, text=str(self.moneyHolder.available_values[0]) + " " + self.moneyHolder.currency, width=15)
        self.window.button1.grid(column=0, row=9)
        self.window.button2 = Button(self.window, text=str(self.moneyHolder.available_values[1]) + " " + self.moneyHolder.currency, width=15)
        self.window.button2.grid(column=0, row=10)
        self.window.button3 = Button(self.window, text=str(self.moneyHolder.available_values[2]) + " " + self.moneyHolder.currency, width=15)
        self.window.button3.grid(column=0, row=11)
        self.window.button4 = Button(self.window, text=str(self.moneyHolder.available_values[3]) + " " + self.moneyHolder.currency, width=15)
        self.window.button4.grid(column=0, row=12)
        self.window.button5 = Button(self.window, text=str(self.moneyHolder.available_values[4]) + " " + self.moneyHolder.currency, width=15)
        self.window.button5.grid(column=0, row=13)
        self.window.button6 = Button(self.window, text=str(self.moneyHolder.available_values[5]) + " " + self.moneyHolder.currency, width=15)
        self.window.button6.grid(column=0, row=14)
        self.window.button7 = Button(self.window, text=str(self.moneyHolder.available_values[6]) + " " + self.moneyHolder.currency, width=15)
        self.window.button7.grid(column=1, row=9)
        self.window.button8 = Button(self.window, text=str(self.moneyHolder.available_values[7]) + " " + self.moneyHolder.currency, width=15)
        self.window.button8.grid(column=1, row=10)
        self.window.button9 = Button(self.window, text=str(self.moneyHolder.available_values[8]) + " " + self.moneyHolder.currency, width=15)
        self.window.button9.grid(column=1, row=11)
        self.window.button10 = Button(self.window, text=str(self.moneyHolder.available_values[9]) + " " + self.moneyHolder.currency, width=15)
        self.window.button10.grid(column=1, row=12)
        self.window.button11 = Button(self.window, text=str(self.moneyHolder.available_values[10]) + " " + self.moneyHolder.currency, width=15)
        self.window.button11.grid(column=1, row=13)
        self.window.button12 = Button(self.window, text=str(self.moneyHolder.available_values[11]) + " " + self.moneyHolder.currency, width=15)
        self.window.button12.grid(column=1, row=14)

    def change_time_setup(self):
        """ Metoda tworzące pola i przyciski pozwalające zmienić czas """
        # pole pozwalające na przestawienie aktualnego czasu
        self.window.change_time = Label(self.window, text="Przestaw aktualny czas: ", width=20)
        self.window.change_time.grid(column=0, row=2)

        # zmiana godziny
        self.window.hour_label = Label(self.window, text="wprowadź godzinę ", width=20)
        self.window.hour_label.grid(column=1, row=2)
        self.window.hour_entry = Entry(self.window, width=2)
        self.window.hour_entry.grid(column=2, row=2)
        self.window.hour_entry.insert(0, "0")

        # zmiana minuty
        self.window.minute_label = Label(self.window, text="wprowadź minutę", width=20)
        self.window.minute_label.grid(column=1, row=3)
        self.window.minute_entry = Entry(self.window, width=2)
        self.window.minute_entry.grid(column=2, row=3)
        self.window.minute_entry.insert(0, "0")

        # przycisk przestawiający aktualny czas
        self.window.change_actual_date_button = Button(self.window, text="Przestaw", width=8)
        self.window.change_actual_date_button.grid(column=1, row=4)

    def init_ui(self):
        """ Metoda inicializująca interfejs parkomatu """

        # numer rejestracyjny pojazdu
        self.window.registration_number_label = Label(self.window, text="Numer rejestracyjny: ", width=20, pady=15)
        self.window.registration_number_label.grid(column=0, row=0)
        self.window.registration_number_entry = Entry(self.window, width=20)
        self.window.registration_number_entry.grid(column=1, row=0)

        # aktualna data
        self.window.actual_date_label_label = Label(self.window, text="Aktualna data: ", width=20)
        self.window.actual_date_label_label.grid(column=0, row=1)
        self.window.actual_date_label = Label(self.window, text="", width=20)
        self.window.actual_date_label.grid(column=1, row=1)

        # data wyjazdu z parkingu
        self.window.departure_label = Label(self.window, text="Data wyjazdu z parkingu: ", width=20, pady=15)
        self.window.departure_label.grid(column=0, row=6)
        self.window.date_of_departure_label = Label(self.window, text="", width=20)
        self.window.date_of_departure_label.grid(column=1, row=6)

        # pole pozwalające zmienić liczbę wrzuconych wrzucanych pieniędzy
        self.window.number_of_money_label = Label(self.window, text="Liczba wrzucanych pieniędzy:", width=21)
        self.window.number_of_money_label.grid(column=0, row=7)
        self.window.number_of_money_entry = Entry(self.window, width=20)
        self.window.number_of_money_entry.grid(column=1, row=7)
        self.window.number_of_money_entry.insert(0, "1")
        self.window.label = Label(self.window, width=20)
        self.window.label.grid(row=8)

        # przycisk Zatwierdź
        self.window.confirm_label = Label(self.window, width=20)
        self.window.confirm_label.grid(row=16)
        self.window.confirm_button = Button(self.window, text="Zatwierdź", width=42, pady=3)
        self.window.confirm_button.grid(column=0, row=17, columnspan=2)

        # pole pokazujące sumę wrzuconych monet
        self.window.sum_label = Label(self.window, text="Wrzucona kwota: ", width=20, font="BOLD", pady=15)
        self.window.sum_label.grid(column=0, row=20)
        self.window.sum_of_money_label = Label(self.window, text="0.00", width=20, font="BOLD")
        self.window.sum_of_money_label.grid(column=1, row=20)

        # metoda tworząca pola i przyciski pozwalające zmienić czas
        self.change_time_setup()

        # metoda tworząca przyciski z pieniędzmi
        self.money_buttons()
