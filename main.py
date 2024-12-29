import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QPushButton
from PyQt6.QtGui import QIcon
from login_window import LoginWindow  # Importujemy wygenerowaną klasę z pliku
from main_window import MainWindow



# Uruchamianie aplikacji
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Okno logowania
    login_dialog = LoginWindow()
   # if login_dialog.exec() == QDialog.DialogCode.Accepted:  # Sprawdzamy, czy logowanie było poprawne
        # Otwieramy główne okno aplikacji
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
