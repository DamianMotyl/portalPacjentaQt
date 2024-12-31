from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PyQt6.QtWidgets import QMessageBox
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

        # Frame 1
        self.frame = QtWidgets.QFrame(self.central_widget)
        self.frame.setGeometry(QtCore.QRect(-10, -20, 970, 101))
        self.frame.setStyleSheet("QFrame{background-color:rgb(250, 247, 241);}")
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        # Label inside Frame 1
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(210, 30, 481, 61))
        font = QtGui.QFont()
        font.setFamily("Fira Code")
        font.setPointSize(20)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet("QLabel{color:rgb(89, 170, 165);}")
        self.label.setText("Witaj w systemie \"E-PACJENT\"")

        # Button inside Frame 1
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(830, 40, 91, 41))
        self.pushButton.setText("Wyloguj")

        # GroupBox
        self.groupBox = QtWidgets.QGroupBox("UMÓW WIZYTĘ LUB BADANIE", self.central_widget)
        self.groupBox.setGeometry(QtCore.QRect(20, 90, 901, 191))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet("QGroupBox{background-color:#DFFFE0}")

        # ComboBoxes and Labels inside GroupBox
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
        self.labelGodzina.setGeometry(QtCore.QRect(550, 40, 71, 16))
        self.labelGodzina.setFont(font)

        self.labelData = QtWidgets.QLabel("Data", self.groupBox)
        self.labelData.setGeometry(QtCore.QRect(730, 40, 49, 16))
        self.labelData.setFont(font)

        # ComboBox for Time instead of QTimeEdit
        self.comboBoxGodzina = QtWidgets.QComboBox(self.groupBox)
        self.comboBoxGodzina.setGeometry(QtCore.QRect(550, 70, 121, 31))
        self.comboBoxGodzina.setFont(font)

        # Populate ComboBox with hours and minutes in 20-minute intervals
        for hour in range(8, 20):
            for minute in range(0, 60, 20):
                time_str = f"{hour:02d}:{minute:02d}"
                self.comboBoxGodzina.addItem(time_str)

        self.dateEdit = QtWidgets.QDateEdit(self.groupBox)
        self.dateEdit.setGeometry(QtCore.QRect(720, 70, 130, 31))
        self.dateEdit.setFont(font)
        self.dateEdit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dateEdit.setCalendarPopup(True)

        # Add Appointment Button
        self.pushButtonDodajWizyte = QtWidgets.QPushButton("Dodaj Wizytę", self.groupBox)
        self.pushButtonDodajWizyte.setGeometry(QtCore.QRect(370, 120, 161, 51))
        self.pushButtonDodajWizyte.setFont(font)
        self.pushButtonDodajWizyte.clicked.connect(self.add_appointment)

        # Frame 2 (Scheduled Appointments)
        self.frame_2 = QtWidgets.QFrame(self.central_widget)
        self.frame_2.setGeometry(QtCore.QRect(20, 300, 901, 291))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        self.label_6 = QtWidgets.QLabel("TWOJE ZAPLANOWANE WIZYTY", self.frame_2)
        self.label_6.setGeometry(QtCore.QRect(20, 10, 251, 16))
        font.setPointSize(12)
        font.setBold(True)
        self.label_6.setFont(font)

        self.tableViewWizyty = QtWidgets.QTableView(self.frame_2)
        self.tableViewWizyty.setGeometry(QtCore.QRect(10, 40, 881, 180))

        self.pushButtonOdwolajWizyte = QtWidgets.QPushButton("Odwołaj Wizytę", self.frame_2)
        self.pushButtonOdwolajWizyte.setGeometry(QtCore.QRect(370, 230, 160, 51))
        self.pushButtonOdwolajWizyte.setFont(font)
        self.pushButtonOdwolajWizyte.clicked.connect(self.cancel_appointment)

        # Frame 3 (Archived Appointments)
        self.frame_3 = QtWidgets.QFrame(self.central_widget)
        self.frame_3.setGeometry(QtCore.QRect(20, 610, 901, 280))
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        self.label_7 = QtWidgets.QLabel("TWOJE ARCHIWALNE WIZYTY", self.frame_3)
        self.label_7.setGeometry(QtCore.QRect(10, 10, 231, 16))
        self.label_7.setFont(font)

        self.tableViewArchiwum = QtWidgets.QTableView(self.frame_3)
        self.tableViewArchiwum.setGeometry(QtCore.QRect(10, 40, 881, 150))

        self.pushButtonEksport = QtWidgets.QPushButton("Eksportuj Wizyty", self.frame_3)
        self.pushButtonEksport.setGeometry(QtCore.QRect(370, 210, 160, 51))
        self.pushButtonEksport.setFont(font)
        self.pushButtonEksport.clicked.connect(self.export_appointments)

        # Set up menu and status bar
        self.menubar = self.menuBar()
        self.statusbar = self.statusBar()

        self.setWindowTitle("E-PACJENT")
        self.setFixedSize(950, 900)

        self.load_specializations()
        self.load_appointments()
        self.load_archives()

        self.show()

    def load_specializations(self):
        query = QSqlQuery()
        if query.exec("SELECT DISTINCT specjalizacja FROM lekarze"):
            while query.next():
                self.comboBoxSpecjalizacja.addItem(query.value(0))
        self.comboBoxSpecjalizacja.currentIndexChanged.connect(self.load_doctors)

    def load_doctors(self):
        selected_specialization = self.comboBoxSpecjalizacja.currentText()
        query = QSqlQuery()
        query.prepare("SELECT lekarz FROM lekarze WHERE specjalizacja = :specjalizacja")
        query.bindValue(":specjalizacja", selected_specialization)
        if query.exec():
            self.comboBoxLekarz.clear()
            while query.next():
                self.comboBoxLekarz.addItem(query.value(0))

    def add_appointment(self):
        specialization = self.comboBoxSpecjalizacja.currentText()
        doctor = self.comboBoxLekarz.currentText()
        time = self.comboBoxGodzina.currentText()
        date = self.dateEdit.date().toString("yyyy-MM-dd")

        if not specialization or not doctor or not time or not date:
            print("Proszę wypełnić wszystkie pola")
            return

        day_of_week = self.dateEdit.date().dayOfWeek()
        print(f"Wybrany dzień tygodnia: {day_of_week}")

        if day_of_week in [6, 7]:  # Sobota lub niedziela
            msg = QMessageBox(self)
            msg.setWindowTitle("Ostrzeżenie")
            msg.setText("Nie można umówić wizyty w weekend (sobota/niedziela) oraz w dni świąteczne.")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
            return

        query = QSqlQuery()
        query.prepare(
            "SELECT COUNT(*) FROM wizyty WHERE lekarz = :lekarz AND data = :data AND godzina = :godzina"
        )
        query.bindValue(":lekarz", doctor)
        query.bindValue(":data", date)
        query.bindValue(":godzina", time)
        if query.exec() and query.next() and query.value(0) > 0:
            print("W tym czasie ta wizyta już istnieje.")
            return

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
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        result = msg_box.exec()

        if result == QMessageBox.StandardButton.No:
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

        # Odświeżenie tabeli z wizytami
        self.load_appointments()

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

    def load_archives(self):
        model = QSqlTableModel()
        model.setTable("archiwum")
        model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        model.select()

        model.setHeaderData(1, QtCore.Qt.Orientation.Horizontal, "Specjalizacja")
        model.setHeaderData(2, QtCore.Qt.Orientation.Horizontal, "Lekarz")
        model.setHeaderData(3, QtCore.Qt.Orientation.Horizontal, "Data")
        model.setHeaderData(4, QtCore.Qt.Orientation.Horizontal, "Godzina")

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

    def export_appointments(self):
        model = self.tableViewArchiwum.model()
        if model is None or model.rowCount() == 0:
            QMessageBox.warning(self, "Błąd", "Brak danych do eksportu.")
            return

        # options = QtWidgets.QFileDialog.Options()
        # file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Zapisz plik", "", "CSV Files (*.csv)",
        #                                                      options=options)
        #
        # if not file_path:
        #     return
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


# Run the application
app = QtWidgets.QApplication([])
window = MainWindow()
app.exec()
