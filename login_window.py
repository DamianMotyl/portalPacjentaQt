import sys
from PyQt6.QtWidgets import (
    QApplication, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QGraphicsView
)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("E-Pacjent - Ekran Logowania")
        self.setFixedSize(500, 360)

        # Ustawienia ikony
        self.setWindowIcon(QIcon("logo.png"))  # Wymień na ścieżkę do swojej ikony

        # Nagłówek
        self.header_label = QLabel('LOGOWANIE DO SYSTEMU "E-PACJENT"')
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_label.setStyleSheet("""
            font-family: 'Fira Code';
            font-size: 16px;
            font-weight: bold;
            color: rgb(89, 170, 165);
            background-color: rgb(250, 247, 241);
        """)
        self.header_label.setFixedHeight(50)

        # Etykiety i pola tekstowe
        self.id_label = QLabel("ID Pacjenta")
        self.id_input = QLineEdit()

        self.password_label = QLabel("Hasło dostępu")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Przycisk logowania
        self.login_button = QPushButton("Zaloguj")
        self.login_button.setStyleSheet("""
            background-color: rgb(230, 230, 230);
            border: 1px solid rgb(200, 200, 200);
            padding: 5px;
        """)
        self.login_button.clicked.connect(self.handle_login)

        # Obrazek
        self.image_label = QLabel()
        pixmap = QPixmap("81075.png")  # Wymień na ścieżkę do swojego obrazka
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Układ siatki dla formularza
        form_layout = QGridLayout()
        form_layout.addWidget(self.id_label, 0, 0)
        form_layout.addWidget(self.id_input, 0, 1)
        form_layout.addWidget(self.password_label, 1, 0)
        form_layout.addWidget(self.password_input, 1, 1)

        # Układ poziomy dla obrazka
        side_layout = QVBoxLayout()
        side_layout.addWidget(self.image_label)

        # Główny układ
        main_layout = QHBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(side_layout)

        # Główny układ pionowy
        layout = QVBoxLayout()
        layout.addWidget(self.header_label)
        layout.addLayout(main_layout)
        layout.addWidget(self.login_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def handle_login(self):
        # Logika logowania
        id_pacjenta = self.id_input.text()
        haslo = self.password_input.text()

        if id_pacjenta == "admin" and haslo == "1234":  # Przykładowa walidacja
            print("Zalogowano pomyślnie!")
            self.accept()
        else:
            print("Błędny login lub hasło!")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = LoginWindow()
    window.show()

    sys.exit(app.exec())
