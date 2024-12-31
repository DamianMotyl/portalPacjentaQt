from PyQt6.QtSql import QSqlDatabase, QSqlQuery

def create_db():
    # Dodaj bazę danych
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("przychodnia.db")

    # Sprawdź, czy połączenie z bazą danych jest udane
    if not db.open():
        print("Nie udało się połączyć z bazą danych")
        return

    query = QSqlQuery()

    # Tworzenie tabeli 'lekarze'
    query.exec('''
    CREATE TABLE IF NOT EXISTS lekarze (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lekarz TEXT NOT NULL,
        specjalizacja TEXT NOT NULL
    )
    ''')

    # Tworzenie tabeli 'wizyty'
    query.exec('''
    CREATE TABLE IF NOT EXISTS wizyty (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        specjalizacja TEXT NOT NULL,
        lekarz TEXT NOT NULL,
        data DATE NOT NULL,
        godzina TIME NOT NULL
    )
    ''')

    # Tworzenie tabeli 'archiwum'
    query.exec('''
    CREATE TABLE IF NOT EXISTS archiwum (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        specjalizacja TEXT NOT NULL,
        lekarz TEXT NOT NULL,
        data DATE NOT NULL,
        godzina TIME NOT NULL
    )
    ''')

    db.close()

    add_sample_doctors_and_archives()


def add_sample_doctors_and_archives():
    # Dodaj przykładowych lekarzy
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("przychodnia.db")

    if not db.open():
        print("Nie udało się połączyć z bazą danych")
        return

    query = QSqlQuery()

    # Dodanie lekarzy z nowymi specjalizacjami
    query.prepare("""
        INSERT INTO lekarze (lekarz, specjalizacja) VALUES
        ('Jan Kowalski', 'Kardiolog'),
        ('Anna Nowak', 'Kardiolog'),
        ('Piotr Zieliński', 'Kardiolog'),
        ('Ewa Mazur', 'Kardiolog'),
        ('Marek Wiśniewski', 'Kardiolog'),
        ('Karolina Adamczyk', 'Pediatra'),
        ('Tomasz Kowal', 'Pediatra'),
        ('Agnieszka Szymańska', 'Pediatra'),
        ('Michał Kaczmarek', 'Neurolog'),
        ('Anna Jabłońska', 'Neurolog'),
        ('Jakub Nowicki', 'Chirurg'),
        ('Magdalena Sienkiewicz', 'Chirurg'),
        ('Piotr Kowalewski', 'Chirurg'),
        ('Anna Dąbrowska', 'Dermatolog'),
        ('Janusz Piotrowski', 'Dermatolog'),
        ('Katarzyna Nowicka', 'Dermatolog'),
        ('Zofia Górska', 'Psychiatra'),
        ('Grzegorz Małecki', 'Psychiatra'),
        ('Aleksandra Zawisza', 'Psychiatra')
    """)
    query.exec()

    query.prepare("""
        INSERT INTO archiwum (specjalizacja, lekarz, data, godzina) VALUES
        ('Kardiolog', 'Jan Kowalski', '2024-01-10', '10:00'),
        ('Pediatra', 'Karolina Adamczyk', '2024-01-11', '11:30'),
        ('Neurolog', 'Michał Kaczmarek', '2023-12-20', '09:45'),
        ('Dermatolog', 'Anna Dąbrowska', '2023-11-15', '12:00'),
        ('Psychiatra', 'Zofia Górska', '2023-10-25', '13:15')
    """)

    query.exec()

    db.close()
