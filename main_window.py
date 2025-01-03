from datetime import datetime
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PyQt6.QtWidgets import QMessageBox, QScrollArea
import  csv
import create_database
import os

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        if not os.path.exists("przychodnia.db"):
            create_database.create_db()

        # Ustawienia bazy danych
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("przychodnia.db")
        if not self.db.open():
            print("Nie udało się połączyć z bazą danych")
            return

        # Central Widget
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidget(self.central_widget)
        self.setCentralWidget(self.scroll_area)

        # Frame 1
        self.frame = QtWidgets.QFrame(self.central_widget)
        self.frame.setGeometry(QtCore.QRect(-10, -20, 970, 101))
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        # Tytuł
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(210, 30, 481, 61))
        font_label = QtGui.QFont()
        font_label.setFamily("Fira Code")
        font_label.setPointSize(20)
        font_label.setBold(True)
        self.label.setFont(font_label)
        self.label.setStyleSheet("QLabel{color:rgb(89, 170, 165);}")
        self.label.setText("Witaj w systemie \"E-PACJENT\"")

        # Przycisk Wyloguj
        self.pushButtonWyloguj = QtWidgets.QPushButton(self.frame)
        self.pushButtonWyloguj.setGeometry(QtCore.QRect(830, 40, 91, 41))
        self.pushButtonWyloguj.setText("Wyloguj")
        fontButton = QtGui.QFont()
        fontButton.setPointSize(12)
        fontButton.setBold(True)
        self.pushButtonWyloguj.setFont(fontButton)
        self.pushButtonWyloguj.clicked.connect(self.logout)

        # GroupBox
        self.groupBox = QtWidgets.QGroupBox("UMÓW WIZYTĘ LUB BADANIE", self.central_widget)
        self.groupBox.setGeometry(QtCore.QRect(20, 90, 901, 191))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet("QGroupBox{background-color:#DFFFE0}")

        # Combo Boxy
        self.labelSpecjalizacja = QtWidgets.QLabel("Specjalizacja", self.groupBox)
        self.labelSpecjalizacja.setGeometry(QtCore.QRect(60, 40, 111, 16))
        font.setPointSize(11)
        font.setBold(True)
        self.labelSpecjalizacja.setFont(font)

        self.labelLekarz = QtWidgets.QLabel("Lekarz", self.groupBox)
        self.labelLekarz.setGeometry(QtCore.QRect(300, 40, 49, 16))
        self.labelLekarz.setFont(font)

        self.comboBoxSpecjalizacja = QtWidgets.QComboBox(self.groupBox)
        self.comboBoxSpecjalizacja.setGeometry(QtCore.QRect(60, 70, 191, 31))
        self.comboBoxSpecjalizacja.setFont(font)

        self.comboBoxLekarz = QtWidgets.QComboBox(self.groupBox)
        self.comboBoxLekarz.setGeometry(QtCore.QRect(300, 70, 191, 31))
        self.comboBoxLekarz.setFont(font)

        self.labelGodzina = QtWidgets.QLabel("Godzina", self.groupBox)
        self.labelGodzina.setGeometry(QtCore.QRect(730, 40, 71, 16))
        self.labelGodzina.setFont(font)

        self.labelData = QtWidgets.QLabel("Data", self.groupBox)
        self.labelData.setGeometry(QtCore.QRect(550, 40, 49, 16))
        self.labelData.setFont(font)

        self.dateEdit = QtWidgets.QDateEdit(self.groupBox)
        self.dateEdit.setGeometry(QtCore.QRect(545, 70, 130, 31))
        self.dateEdit.setFont(font)
        self.dateEdit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dateEdit.setMinimumDate(QtCore.QDate.currentDate())
        self.dateEdit.setCalendarPopup(True)

        self.comboBoxGodzina = QtWidgets.QComboBox(self.groupBox)
        self.comboBoxGodzina.setGeometry(QtCore.QRect(725, 70, 121, 31))
        self.comboBoxGodzina.setFont(font)

        current_time = datetime.now()
        selected_date = self.dateEdit.date()
        today_date = QtCore.QDate.currentDate()

    #Wybór godziny póżniejszej niż obecna
        if selected_date == today_date:
            hour = current_time.hour
            minute = current_time.minute
            for h in range(hour, 20):
                for m in range(0, 60, 20):
                    if h == hour and m < minute:
                        continue
                    time_str = f"{h:02d}:{m:02d}"
                    self.comboBoxGodzina.addItem(time_str)
        else:
            for h in range(8, 20):
                for m in range(0, 60, 20):
                    time_str = f"{h:02d}:{m:02d}"
                    self.comboBoxGodzina.addItem(time_str)

        # Aktualizacja comboBox przy zmianie daty
        self.dateEdit.dateChanged.connect(lambda: self.comboBoxGodzina.clear() or [
            self.comboBoxGodzina.addItem(
                f"{h:02d}:{m:02d}") for h in
            (range(current_time.hour, 20) if self.dateEdit.date() == today_date else range(8, 20)) for m in
            range(0, 60, 20) if self.dateEdit.date() != today_date or h != current_time.hour or m >= current_time.minute
        ])


        # Dodaj Wizyte - przycisk
        self.pushButtonDodajWizyte = QtWidgets.QPushButton("Dodaj Wizytę", self.groupBox)
        self.pushButtonDodajWizyte.setGeometry(QtCore.QRect(370, 120, 161, 51))
        self.pushButtonDodajWizyte.setFont(font)
        self.pushButtonDodajWizyte.clicked.connect(self.add_appointment)

        # Frame 2
        self.frame_2 = QtWidgets.QFrame(self.central_widget)
        self.frame_2.setGeometry(QtCore.QRect(20, 300, 901, 291))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        self.label_6 = QtWidgets.QLabel("TWOJE ZAPLANOWANE WIZYTY", self.frame_2)
        self.label_6.setGeometry(QtCore.QRect(20, 10, 251, 16))
        font.setPointSize(12)
        font.setBold(True)
        self.label_6.setFont(font)

        #Tabela Wizyty
        self.tableViewWizyty = QtWidgets.QTableView(self.frame_2)
        self.tableViewWizyty.setGeometry(QtCore.QRect(10, 40, 881, 180))

        #Przycisk - Odwołaj Wizytę
        self.pushButtonOdwolajWizyte = QtWidgets.QPushButton("Odwołaj Wizytę", self.frame_2)
        self.pushButtonOdwolajWizyte.setGeometry(QtCore.QRect(370, 230, 160, 51))
        self.pushButtonOdwolajWizyte.setFont(font)
        self.pushButtonOdwolajWizyte.clicked.connect(self.cancel_appointment)

        # Frame 3
        self.frame_3 = QtWidgets.QFrame(self.central_widget)
        self.frame_3.setGeometry(QtCore.QRect(20, 610, 901, 350))
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        self.label_7 = QtWidgets.QLabel("TWOJE ARCHIWALNE WIZYTY", self.frame_3)
        self.label_7.setGeometry(QtCore.QRect(10, 10, 231, 16))
        self.label_7.setFont(font)

        self.label_8 = QtWidgets.QLabel("Filtruj wizyty:", self.frame_3)
        self.label_8.setGeometry(QtCore.QRect(20, 35, 231, 25))
        self.label_8.setFont(font)

        #Tabela Archiwum
        self.tableViewArchiwum = QtWidgets.QTableView(self.frame_3)
        self.tableViewArchiwum.setGeometry(QtCore.QRect(10, 100, 881, 150))

        # Przycisk Export do CSV
        self.pushButtonEksport = QtWidgets.QPushButton("Eksportuj Wizyty", self.frame_3)
        self.pushButtonEksport.setGeometry(QtCore.QRect(370, 265, 160, 51))
        self.pushButtonEksport.setFont(font)
        self.pushButtonEksport.clicked.connect(self.export_appointments)

        #Combo Boxy do filtrowania
        self.filterSpecjalizacja = QtWidgets.QComboBox(self.frame_3)
        self.filterSpecjalizacja.setGeometry(QtCore.QRect(20, 65, 191, 31))
        self.filterSpecjalizacja.setFont(font)
        self.filterSpecjalizacja.addItem("Specjalizacja")
        self.filterSpecjalizacja.currentIndexChanged.connect(self.apply_filter)

        self.filterLekarz = QtWidgets.QComboBox(self.frame_3)
        self.filterLekarz.setGeometry(QtCore.QRect(240, 65, 191, 31))
        self.filterLekarz.setFont(font)
        self.filterLekarz.addItem("Lekarz")
        self.filterLekarz.currentIndexChanged.connect(self.apply_filter)

        self.filterData = QtWidgets.QComboBox(self.frame_3)
        self.filterData.setGeometry(QtCore.QRect(460, 65, 191, 31))
        self.filterData.setFont(font)
        self.filterData.addItem("Data")
        self.filterData.currentIndexChanged.connect(self.apply_filter)

        self.menubar = self.menuBar()
        self.statusbar = self.statusBar()

        self.setWindowTitle("E-PACJENT")
        self.setFixedSize(950, 950)
        self.setWindowIcon(QIcon("medi.png"))

        self.load_specializations()
        self.load_appointments()
        self.load_archives()
        self.archive_past_appointments()

        #timer do aktualizacji wizyt
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.archive_past_appointments)
        self.timer.start(20*30*1000)

        self.show()

    #Wczytanie specjalizacji do combobox
    def load_specializations(self):
        self.comboBoxSpecjalizacja.addItem("")
        query = QSqlQuery()
        if query.exec("SELECT DISTINCT specjalizacja FROM lekarze"):
            while query.next():
                self.comboBoxSpecjalizacja.addItem(query.value(0))

        self.comboBoxSpecjalizacja.currentIndexChanged.connect(self.load_doctors)

    #Załadowanie lekarzy do combobox
    def load_doctors(self):
        selected_specialization = self.comboBoxSpecjalizacja.currentText()
        query = QSqlQuery()
        query.prepare("SELECT lekarz FROM lekarze WHERE specjalizacja = :specjalizacja")
        query.bindValue(":specjalizacja", selected_specialization)
        if query.exec():
            self.comboBoxLekarz.clear()
            while query.next():
                self.comboBoxLekarz.addItem(query.value(0))

    #Dodanie wizyty
    def add_appointment(self):
        specialization = self.comboBoxSpecjalizacja.currentText()
        doctor = self.comboBoxLekarz.currentText()
        time = self.comboBoxGodzina.currentText()
        date = self.dateEdit.date().toString("yyyy-MM-dd")

        if not specialization or not doctor or not time or not date:
            msgbox = QMessageBox(self)
            msgbox.setWindowTitle("Uwaga")
            msgbox.setText("Proszę uzupełnić wszystkie pola.")
            msgbox.setIcon(QMessageBox.Icon.Information)
            msgbox.setStandardButtons(QMessageBox.StandardButton.Ok)
            msgbox.exec()
            return

        #Pomięcie weekendów oraz świąt
        day_of_week = self.dateEdit.date().dayOfWeek()
        date_of_visit = self.dateEdit.date().toString("MM-dd")
        holidays = [
            "01-01",
            "01-06",
            "04-20",
            "04-21",
            "05-01",
            "05-03",
            "06-08",
            "06-19",
            "08-15",
            "11-01",
            "11-11",
            "12-25",
            "12-26"
        ]

        if day_of_week in [6, 7] or date_of_visit in holidays:  # Sobota lub niedziela
            msg = QMessageBox(self)
            msg.setWindowTitle("Ostrzeżenie")
            msg.setText("Nie można umówić wizyty w weekend (sobota/niedziela) oraz w dni świąteczne.")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
            return

        #Sprawdzenie czy o tej godzinie nie ma już wizyty
        query = QSqlQuery()
        query.prepare(
            "SELECT COUNT(*) FROM wizyty WHERE data = :data AND godzina = :godzina"
        )
        query.bindValue(":lekarz", doctor)
        query.bindValue(":data", date)
        query.bindValue(":godzina", time)
        if query.exec() and query.next() and query.value(0) > 0:
            msgbox = QMessageBox(self)
            msgbox.setWindowTitle("Uwaga")
            msgbox.setText("O tej godzinie masz juz zarezerwowaną wizytę.")
            msgbox.setIcon(QMessageBox.Icon.Information)
            msgbox.setStandardButtons(QMessageBox.StandardButton.Ok)
            msgbox.exec()
            return

        #Daodanie wizyty do tabeli
        query.prepare(
            "INSERT INTO wizyty (specjalizacja, lekarz, godzina, data) VALUES (:specjalizacja, :lekarz, :godzina, :data)"
        )
        query.bindValue(":specjalizacja", specialization)
        query.bindValue(":lekarz", doctor)
        query.bindValue(":godzina", time)
        query.bindValue(":data", date)
        if query.exec():
            print("Wizyta dodana pomyślnie")
        else:
            print("Błąd podczas dodawania wizyty")
        self.load_appointments()

    #Odwołanie wizyty
    def cancel_appointment(self):
        selected_row = self.tableViewWizyty.selectionModel().currentIndex().row()

        if selected_row < 0:
            msg = QMessageBox(self)
            msg.setWindowTitle("Błąd")
            msg.setText("Proszę wybrać wizytę do odwołania.")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
            return

        # Pobranie szczegółów wizyty z modelu
        model = self.tableViewWizyty.model()
        specialization = model.index(selected_row, 1).data()
        doctor = model.index(selected_row, 2).data()
        date = model.index(selected_row, 3).data()
        time = model.index(selected_row, 4).data()

        # Potwierdzenie usunięcia
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Potwierdzenie")
        msg_box.setText(
            f"Czy na pewno chcesz odwołać wizytę?\n\nSpecjalizacja: {specialization}\nLekarz: {doctor}\nData: {date}\nGodzina: {time}")
        msg_box.setIcon(QMessageBox.Icon.Question)

        ok_button = msg_box.addButton("Tak", QMessageBox.ButtonRole.AcceptRole)
        cancel_button = msg_box.addButton("Nie", QMessageBox.ButtonRole.RejectRole)
        result = msg_box.exec()

        if msg_box.clickedButton() == cancel_button:
            return

        # Usunięcie wizyty z bazy danych
        query = QSqlQuery()
        query.prepare(
            "DELETE FROM wizyty WHERE specjalizacja = :specjalizacja AND lekarz = :lekarz AND data = :data AND godzina = :godzina"
        )
        query.bindValue(":specjalizacja", specialization)
        query.bindValue(":lekarz", doctor)
        query.bindValue(":data", date)
        query.bindValue(":godzina", time)

        if query.exec():
            print("Wizyta została odwołana.")
        else:
            print("Błąd podczas odwoływania wizyty.")

        self.load_appointments()

    #Wyświetalnie danych z tabeli wizyty
    def load_appointments(self):
        model = QSqlTableModel()
        model.setTable("wizyty")
        model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        model.select()

        model.setHeaderData(1, QtCore.Qt.Orientation.Horizontal, "Specjalizacja")
        model.setHeaderData(2, QtCore.Qt.Orientation.Horizontal, "Lekarz")
        model.setHeaderData(3, QtCore.Qt.Orientation.Horizontal, "Data")
        model.setHeaderData(4, QtCore.Qt.Orientation.Horizontal, "Godzina")

        # Ustawienia tabeli
        self.tableViewWizyty.setModel(model)
        self.tableViewWizyty.hideColumn(0)
        header = self.tableViewWizyty.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableViewWizyty.setStyleSheet(
            """
            QTableView {
                font-size: 10pt;
                background-color: #f9f9f9;
                alternate-background-color: #e6f4f1;
                gridline-color: #c3c3c3;
            }
            QHeaderView::section {
                background-color: #89aaa5;
                color: white;
                font-weight: bold;
                font-size: 11pt;
                border: 1px solid #d4d4d4;
                padding: 4px;
            }
            """
        )
        self.tableViewWizyty.horizontalHeader().setStretchLastSection(True)  # Rozciąganie ostatniej kolumny
        self.tableViewWizyty.verticalHeader().setVisible(False)  # Ukrycie opisów wierszy
        self.tableViewWizyty.setSelectionBehavior(QtWidgets.QTableView.SelectionBehavior.SelectRows)  # Wybór całych wierszy
        self.tableViewWizyty.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)  # Zablokowanie edycji
        self.tableViewWizyty.setSortingEnabled(True)  # Sortowanie po kliknięciu w nagłówek kolumny

    #Załadowanie wizyt archiwalnych
    def load_archives(self):
        model = QSqlTableModel()
        model.setTable("archiwum")
        model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        model.select()

        model.setHeaderData(1, QtCore.Qt.Orientation.Horizontal, "Specjalizacja")
        model.setHeaderData(2, QtCore.Qt.Orientation.Horizontal, "Lekarz")
        model.setHeaderData(3, QtCore.Qt.Orientation.Horizontal, "Data")
        model.setHeaderData(4, QtCore.Qt.Orientation.Horizontal, "Godzina")

        query = QSqlQuery("SELECT DISTINCT specjalizacja FROM archiwum")
        while query.next():
            self.filterSpecjalizacja.addItem(query.value(0))

        query = QSqlQuery("SELECT DISTINCT lekarz FROM archiwum")
        while query.next():
            self.filterLekarz.addItem(query.value(0))

        query = QSqlQuery("SELECT DISTINCT data FROM archiwum")
        while query.next():
            self.filterData.addItem(query.value(0))

        # Ustawienia tabeli
        self.tableViewArchiwum.setModel(model)
        self.tableViewArchiwum.hideColumn(0)
        header = self.tableViewArchiwum.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableViewArchiwum.setStyleSheet(
            """
            QTableView {
                font-size: 10pt;
                background-color: #f9f9f9;
                alternate-background-color: #e6f4f1;
                gridline-color: #c3c3c3;
            }
            QHeaderView::section {
                background-color: #89aaa5;
                color: white;
                font-weight: bold;
                font-size: 11pt;
                border: 1px solid #d4d4d4;
                padding: 4px;
            }
            """
        )
        self.tableViewArchiwum.horizontalHeader().setStretchLastSection(True)  # Rozciąganie ostatniej kolumny
        self.tableViewArchiwum.verticalHeader().setVisible(False)  # Ukrycie opisów wierszy
        self.tableViewArchiwum.setSelectionBehavior(QtWidgets.QTableView.SelectionBehavior.SelectRows)  # Wybór całych wierszy
        self.tableViewArchiwum.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)  # Zablokowanie edycji
        self.tableViewArchiwum.setSortingEnabled(True)  # Sortowanie po kliknięciu w nagłówek kolumny

    #Export wizyt archiwalnych do pliku
    def export_appointments(self):
        model = self.tableViewArchiwum.model()
        if model is None or model.rowCount() == 0:
            QMessageBox.warning(self, "Błąd", "Brak danych do eksportu.")
            return

        app_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(app_directory, "archiwum_wizyt.csv")

        try:
            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                # Zapis nagłówków
                headers = [model.headerData(i, Qt.Orientation.Horizontal) for i in range(model.columnCount())]
                writer.writerow(headers)
                # Zapis danych
                for row in range(model.rowCount()):
                    row_data = [model.index(row, col).data() for col in range(model.columnCount())]
                    writer.writerow(row_data)

            QMessageBox.information(self, "Sukces", "Wizyty zostały pomyślnie wyeksportowane.")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas eksportu: {str(e)}")

    #Filtrowanie tabeli
    def apply_filter(self):
        model = self.tableViewArchiwum.model()
        filter_query = []

        if self.filterSpecjalizacja.currentText() != "Specjalizacja":
            filter_query.append(f"specjalizacja = '{self.filterSpecjalizacja.currentText()}'")

        if self.filterLekarz.currentText() != "Lekarz":
            filter_query.append(f"lekarz = '{self.filterLekarz.currentText()}'")

        if self.filterData.currentText() != "Data":
            filter_query.append(f"data = '{self.filterData.currentText()}'")

        if filter_query:
            model.setFilter(" AND ".join(filter_query))
        else:
            model.setFilter("")

        model.select()

    #wylogowanie
    def logout(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Potwierdzenie wylogowania")
        msg_box.setText("Czy na pewno chcesz się wylogować?")
        msg_box.setIcon(QMessageBox.Icon.Question)
        ok_button = msg_box.addButton("Tak", QMessageBox.ButtonRole.AcceptRole)
        cancel_button = msg_box.addButton("Nie", QMessageBox.ButtonRole.RejectRole)

        result = msg_box.exec()

        if msg_box.clickedButton() == ok_button:
            print("Użytkownik został wylogowany.")
            self.close()
        else:
            print("Anulowano wylogowanie.")

    def archive_past_appointments(self):
        current_datetime = datetime.now()
        current_date = current_datetime.strftime("%Y-%m-%d")
        current_time = current_datetime.strftime("%H:%M")

        query = QSqlQuery()
        query.prepare("""
            SELECT * FROM wizyty
            WHERE data < :current_date
            OR (data = :current_date AND godzina < :current_time)
        """)
        query.bindValue(":current_date", current_date)
        query.bindValue(":current_time", current_time)

        if query.exec():
            while query.next():
                id_wizyty = query.value(0)
                specjalizacja = query.value(1)
                lekarz = query.value(2)
                data = query.value(3)
                godzina = query.value(4)

                archive_query = QSqlQuery()
                archive_query.prepare("""
                    INSERT INTO archiwum (specjalizacja, lekarz, data, godzina)
                    VALUES (:specjalizacja, :lekarz, :data, :godzina)
                """)
                archive_query.bindValue(":specjalizacja", specjalizacja)
                archive_query.bindValue(":lekarz", lekarz)
                archive_query.bindValue(":data", data)
                archive_query.bindValue(":godzina", godzina)

                if not archive_query.exec():
                    print("Błąd podczas przenoszenia wizyty do archiwum.")

                # Usuń z tabeli wizyty
                delete_query = QSqlQuery()
                delete_query.prepare("DELETE FROM wizyty WHERE id = :id")
                delete_query.bindValue(":id", id_wizyty)

                if not delete_query.exec():
                    print("Błąd podczas usuwania wizyty z głównej tabeli.")

        self.load_appointments()
        self.load_archives()