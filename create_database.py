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

    add_sample_doctors()


def add_sample_doctors():
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

    db.close()
