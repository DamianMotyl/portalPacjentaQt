import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QPushButton
from PyQt6.QtGui import QIcon
from login_window import LoginWindow  # Importujemy wygenerowaną klasę z pliku
from main_window import MainWindow

# Uruchamianie aplikacji
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QPushButton {
            background-color: #e1eae8; /* Niebieskie przyciski */
            border: 1px solid #89aaa5;
            border-radius: 5px;
            padding: 5px 10px;
        }
        QPushButton:hover {
            background-color: #f0f4f4; /* Jaśniejszy niebieski po najechaniu */
        }
        QPushButton:pressed {
            background-color: #1F618D; /* Ciemniejszy niebieski po kliknięciu */
            }
    """)

    login_dialog = LoginWindow()
    if login_dialog.exec() == QDialog.DialogCode.Accepted:
        main_window = MainWindow()
        main_window.show()
    sys.exit(app.exec())
