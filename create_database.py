from PyQt6.QtSql import QSqlDatabase, QSqlQuery

def create_db():
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("przychodnia.db")

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
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("przychodnia.db")

    if not db.open():
        print("Nie udało się połączyć z bazą danych")
        return

    query = QSqlQuery()
    query.prepare("""
        INSERT INTO lekarze (lekarz, specjalizacja) VALUES
        ('Jan Kowalski', 'Kardiolog'),
        ('Anna Nowak', 'Kardiolog'),
        ('Piotr Zieliński', 'Kardiolog'),
        ('Ewa Mazur', 'Kardiolog'),
        ('Marek Wiśniewski', 'Kardiolog'),
        ('Karolina Adamczyk', 'Gastrolog'),
        ('Tomasz Kowal', 'Gastrolog'),
        ('Agnieszka Szymańska', 'Gastrolog'),
        ('Michał Kaczmarek', 'Neurolog'),
        ('Anna Jabłońska', 'Neurolog'),
        ('Jakub Nowicki', 'Chirurg'),
        ('Magdalena Sienkiewicz', 'Chirurg'),
        ('Piotr Kowalewski', 'Chirurg'),
        ('Anna Dąbrowska', 'Dermatolog'),
        ('Janusz Piotrowski', 'Dermatolog'),
        ('Katarzyna Nowicka', 'Dermatolog'),
        ('Zofia Górska', 'Laryngolog'),
        ('Grzegorz Małecki', 'Laryngolog'),
        ('Aleksandra Zawisza', 'Laryngolog')
    """)
    query.exec()

    query.prepare("""
        INSERT INTO archiwum (specjalizacja, lekarz, data, godzina) VALUES
        ('Kardiolog', 'Jan Kowalski', '2024-01-10', '10:00'),
        ('Gastrolog', 'Karolina Adamczyk', '2024-01-11', '11:30'),
        ('Neurolog', 'Michał Kaczmarek', '2023-12-20', '09:45'),
        ('Dermatolog', 'Anna Dąbrowska', '2023-11-15', '12:00'),
        ('Laryngolog', 'Zofia Górska', '2023-10-25', '13:15'),
        ('Kardiolog', 'Jan Kowalski', '2024-02-01', '10:30'),
        ('Kardiolog', 'Jan Kowalski', '2024-02-03', '14:00'),
        ('Gastrolog', 'Tomasz Kowal', '2024-02-03', '09:00'),
        ('Neurolog', 'Anna Jabłońska', '2024-02-05', '16:00'),
        ('Chirurg', 'Jakub Nowicki', '2024-02-06', '11:00'),
        ('Chirurg', 'Magdalena Sienkiewicz', '2024-02-07', '15:00'),
        ('Dermatolog', 'Anna Dąbrowska', '2024-02-08', '13:00'),
        ('Laryngolog', 'Grzegorz Małecki', '2024-02-10', '10:15'),
        ('Chirurg', 'Piotr Kowalewski', '2024-02-12', '12:30'),
        ('Dermatolog', 'Katarzyna Nowicka', '2024-02-15', '14:00'),
        ('Neurolog', 'Michał Kaczmarek', '2024-02-16', '09:30'),
        ('Kardiolog', 'Marek Wiśniewski', '2024-02-18', '08:00')
    """)

    query.exec()
    db.close()
