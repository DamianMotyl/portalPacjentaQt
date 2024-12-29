from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
import create_database
import os

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        if not os.path.exists("przychodnia.db"):
            create_database.create_db()

        # Central Widget
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Frame 1
        self.frame = QtWidgets.QFrame(self.central_widget)
        self.frame.setGeometry(QtCore.QRect(-10, -20, 941, 101))
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
        self.groupBox.setGeometry(QtCore.QRect(20, 100, 901, 191))
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
        for hour in range(24):
            for minute in range(0, 60, 20):
                time_str = f"{hour:02d}:{minute:02d}"
                self.comboBoxGodzina.addItem(time_str)

        self.dateEdit = QtWidgets.QDateEdit(self.groupBox)
        self.dateEdit.setGeometry(QtCore.QRect(720, 70, 130, 31))
        self.dateEdit.setFont(font  )
        self.dateEdit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dateEdit.setCalendarPopup(True)

        # Add Appointment Button
        self.pushButtonDodajWizyte = QtWidgets.QPushButton("Dodaj Wizytę", self.groupBox)
        self.pushButtonDodajWizyte.setGeometry(QtCore.QRect(370, 120, 161, 51))
        self.pushButtonDodajWizyte.setFont(font)

        # Frame 2 (Scheduled Appointments)
        self.frame_2 = QtWidgets.QFrame(self.central_widget)
        self.frame_2.setGeometry(QtCore.QRect(20, 320, 901, 241))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        self.label_6 = QtWidgets.QLabel("TWOJE ZAPLANOWANE WIZYTY", self.frame_2)
        self.label_6.setGeometry(QtCore.QRect(20, 10, 251, 16))
        font.setPointSize(12)
        font.setBold(True)
        self.label_6.setFont(font)

        self.tableView_2 = QtWidgets.QTableView(self.frame_2)
        self.tableView_2.setGeometry(QtCore.QRect(10, 40, 881, 131))

        self.pushButtonOdwolajWizyte = QtWidgets.QPushButton("Odwołaj Wizytę", self.frame_2)
        self.pushButtonOdwolajWizyte.setGeometry(QtCore.QRect(370, 180, 160, 51))
        self.pushButtonOdwolajWizyte.setFont(font)

        # Frame 3 (Archived Appointments)
        self.frame_3 = QtWidgets.QFrame(self.central_widget)
        self.frame_3.setGeometry(QtCore.QRect(20, 580, 901, 191))
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)

        self.label_7 = QtWidgets.QLabel("TWOJE ARCHIWALNE WIZYTY", self.frame_3)
        self.label_7.setGeometry(QtCore.QRect(10, 10, 231, 16))
        self.label_7.setFont(font)

        self.tableView = QtWidgets.QTableView(self.frame_3)
        self.tableView.setGeometry(QtCore.QRect(10, 40, 881, 131))

        # Set up menu and status bar
        self.menubar = self.menuBar()
        self.statusbar = self.statusBar()

        self.setWindowTitle("E-PACJENT")
        self.setFixedSize(950, 900)

        self.load_specializations()

        self.show()

    def load_specializations(self):
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("przychodnia.db")

        if not db.open():
            print("Nie udało się połączyć z bazą danych")
            return

        query = QSqlQuery()

        # Pobranie wszystkich unikalnych specjalizacji z tabeli lekarzy
        query.exec("SELECT DISTINCT specjalizacja FROM lekarze")
        while query.next():
            self.comboBoxSpecjalizacja.addItem(query.value(0))

        # Obsługuje zmianę wybranej specjalizacji, aby wczytać odpowiednich lekarzy
        self.comboBoxSpecjalizacja.currentIndexChanged.connect(self.load_doctors)

        db.close()

    def load_doctors(self):
        # Załaduj lekarzy na podstawie wybranej specjalizacji
        selected_specialization = self.comboBoxSpecjalizacja.currentText()
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("przychodnia.db")

        if not db.open():
            print("Nie udało się połączyć z bazą danych")
            return

        query = QSqlQuery()

        # Pobranie lekarzy z wybranej specjalizacji
        query.prepare("SELECT lekarz FROM lekarze WHERE specjalizacja = :specjalizacja")
        query.bindValue(":specjalizacja", selected_specialization)
        query.exec()

        self.comboBoxLekarz.clear()  # Wyczyszczenie poprzednich danych

        while query.next():
            self.comboBoxLekarz.addItem(query.value(0))

        db.close()

# Run the application
app = QtWidgets.QApplication([])
window = MainWindow()
app.exec()
