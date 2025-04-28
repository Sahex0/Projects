import pyodbc
import requests
import openpyxl
from difflib import SequenceMatcher

# Datenbankverbindung herstellen
connection = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=bibliomind.database.windows.net;'  
    'DATABASE=bibliomind;'      
    'Authentication=ActiveDirectoryInteractive;'
    'UID=nico.hemmer@edu.szu.at;'                
)
cursor = connection.cursor()

# API URL (Open Library API)
API_URL = "https://openlibrary.org/api/books?bibkeys=ISBN:{}&format=json"

# Funktion zur Bereinigung und Überprüfung von ISBN-Nummern
def clean_isbn(isbn):
    if not isbn:  # Prüfen, ob ISBN None oder leer ist
        return None
    return ''.join(filter(str.isdigit, isbn))  # Entfernt Nicht-Zahlen

# Funktion zur Überprüfung der Ähnlichkeit von Titeln
def is_title_similar(title1, title2, tolerance=0.3):
    if not title1 or not title2:
        return False
    similarity = SequenceMatcher(None, title1.lower(), title2.lower()).ratio()
    return similarity >= (1 - tolerance)

# Excel-Datei und Arbeitsblatt vorbereiten
wb = openpyxl.Workbook()
sheet = wb.active
sheet.title = "ISBN-Überprüfung"
sheet.append(["MEDIENNR", "ISBN", "Status", "Titelvergleich"])

# Alle ISBNs aus der Tabelle MEDIEN abrufen
query = "SELECT MEDIENNR, ISBN, HST FROM MEDIEN"
cursor.execute(query)
rows = cursor.fetchall()

for row in rows:
    mediennr = row.MEDIENNR
    isbn_raw = row.ISBN
    title_db = row.HST

    if isbn_raw is None:
        sheet.append((mediennr, None, "Keine ISBN vorhanden", "Keine Überprüfung"))
        wb.save("isbn_ergebnisse.xlsx")
        continue

    isbn_cleaned = clean_isbn(isbn_raw)

    if not isbn_cleaned or len(isbn_cleaned) not in [10, 13]:
        sheet.append((mediennr, isbn_raw, "Ungültiges Format", "Keine Überprüfung"))
        wb.save("isbn_ergebnisse.xlsx")
        continue

    # API-Abfrage
    response = requests.get(API_URL.format(isbn_cleaned))
    if response.status_code == 200:
        data = response.json()
        if f"ISBN:{isbn_cleaned}" in data:
            api_data = data[f"ISBN:{isbn_cleaned}"]
            title_api = api_data.get("info_url", "").split('/')[-1].replace('_', ' ')

            if is_title_similar(title_db, title_api):
                sheet.append((mediennr, isbn_raw, "Gültig", "Titel stimmt überein"))
                print((mediennr, isbn_raw, "Gültig", "Titel stimmt überein"))
            else:
                sheet.append((mediennr, isbn_raw, "Gültig", "Titel stimmt nicht überein"))
                print((mediennr, isbn_raw, "Gültig", "Titel stimmt nicht überein"))
        else:
            sheet.append((mediennr, isbn_raw, "Nicht gefunden", "Keine Überprüfung"))
            print((mediennr, isbn_raw, "Nicht gefunden", "Keine Überprüfung"))
    else:
        sheet.append((mediennr, isbn_raw, "API-Fehler", "Keine Überprüfung"))
        print((mediennr, isbn_raw, "API-Fehler", "Keine Überprüfung"))

    # Excel-Datei nach jeder Zeile speichern
    wb.save("isbn_ergebnisse.xlsx")

# Verbindung zur Datenbank schließen
cursor.close()
connection.close()

print("Überprüfung abgeschlossen. Ergebnisse wurden in 'isbn_ergebnisse.xlsx' gespeichert.")
