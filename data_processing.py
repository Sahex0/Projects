import pyodbc
from datetime import datetime

# Verbindung zu SQL Server herstellen
def connect_to_database():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=bibliomind.database.windows.net;'
        'DATABASE=bibliomind;'
        'Authentication=ActiveDirectoryInteractive;'
        'UID=ahmethan.oezbek@edu.szu.at;'
    )

class DatabaseHandler:
    def __init__(self):
        self.connection = connect_to_database()
        self.cursor = self.connection.cursor()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

    # Funktion zur automatischen Generierung einer eindeutigen Mediennummer
    def generate_mediennr(self):
        try:
            self.cursor.execute("SELECT top 1 CAST(MEDIENNR as int) FROM dbo.Medien order by Cast(Mediennr as int) desc")
            max_mediennr_row = self.cursor.fetchone()
            max_mediennr = max_mediennr_row[0] or 0  # Falls keine Mediennummer existiert, beginne bei 0
            return max_mediennr + 1  # Rückgabe als Integer
        except Exception as e:
            return f"Fehler bei der Generierung der Mediennummer: {e}"

    # Funktion zur automatischen Generierung einer eindeutigen Exemplarnummer
    def generate_exemplarnr(self):
        try:
            self.cursor.execute("SELECT MAX(EXEMPLARNR) FROM dbo.Exemplar")
            max_exemplarnr_row = self.cursor.fetchone()
            max_exemplarnr = max_exemplarnr_row[0] or 0  # Falls keine Exemplarnummer existiert, beginne bei 0
            return max_exemplarnr + 1
        except Exception as e:
            return f"Fehler bei der Generierung der Exemplarnummer: {e}"

    # Funktion zur Überprüfung, ob eine Mediennummer existiert
    def is_valid_mediennr(self, mediennr):
        self.cursor.execute("SELECT 1 FROM dbo.Medien WHERE MEDIENNR = ?", (mediennr,))
        return self.cursor.fetchone() is not None

    # Funktion zur Überprüfung, ob eine Exemplarnummer existiert
    def is_valid_exemplarnr(self, exemplarnr):
        self.cursor.execute("SELECT 1 FROM dbo.Exemplar WHERE EXEMPLARNR = ?", (exemplarnr,))
        return self.cursor.fetchone() is not None

    # Funktionen für Medien
    def add_medien(self, art, verf1, hst, syst, mediengrp, jahr, isbn):
        mediennr = self.generate_mediennr()
        if mediennr is None:
            return "Mediennummer konnte nicht generiert werden."

        try:
            insert_query = """
            INSERT INTO dbo.Medien (MEDIENNR, ART, VERF1, HST, SYST, MEDIENGRP, JAHR, ISBN)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            self.cursor.execute(insert_query, (mediennr, art, verf1, hst, syst, mediengrp, jahr, isbn))
            self.connection.commit()
            return f"Neuer Eintrag in Medien mit MEDIENNR {mediennr} hinzugefügt."
        except Exception as e:
            return f"Fehler beim Hinzufügen des Eintrags in Medien: {e}"

    def delete_medien(self, mediennr):
        if not self.is_valid_mediennr(mediennr):
            return "Fehler: Die eingegebene Mediennummer ist ungültig."

        try:
            # Lösche alle Einträge in Exemplar, die mit der Mediennummer verknüpft sind
            delete_exemplar_query = "DELETE FROM dbo.Exemplar WHERE MEDIENNREX = ?"
            self.cursor.execute(delete_exemplar_query, (mediennr,))

            # Lösche den Eintrag in Medien
            delete_medien_query = "DELETE FROM dbo.Medien WHERE MEDIENNR = ?"
            self.cursor.execute(delete_medien_query, (mediennr,))

            self.connection.commit()
            return f"Eintrag in Medien mit MEDIENNR {mediennr} und zugehörige Exemplare gelöscht."
        except Exception as e:
            return f"Fehler beim Löschen des Eintrags in Medien und zugehöriger Exemplare: {e}"

    def update_medien(self, mediennr, art=None, verf1=None, hst=None, syst=None, mediengrp=None, jahr=None, isbn=None):
        if not self.is_valid_mediennr(mediennr):
            return "Fehler: Die eingegebene Mediennummer ist ungültig."

        try:
            update_query = "UPDATE dbo.Medien SET "
            params = []
            if art:
                update_query += "ART = ?, "
                params.append(art)
            if verf1:
                update_query += "VERF1 = ?, "
                params.append(verf1)
            if hst:
                update_query += "HST = ?, "
                params.append(hst)
            if syst:
                update_query += "SYST = ?, "
                params.append(syst)
            if mediengrp:
                update_query += "MEDIENGRP = ?, "
                params.append(mediengrp)
            if jahr:
                update_query += "JAHR = ?, "
                params.append(jahr)
            if isbn:
                update_query += "ISBN = ?, "
                params.append(isbn)

            update_query = update_query.rstrip(", ") + " WHERE MEDIENNR = ?"
            params.append(mediennr)

            self.cursor.execute(update_query, params)
            self.connection.commit()
            return f"Eintrag in Medien mit MEDIENNR {mediennr} aktualisiert."
        except Exception as e:
            return f"Fehler beim Bearbeiten des Eintrags in Medien: {e}"

    # Funktionen für Exemplar
    def add_exemplar(self, mediennrex, zugangsdatum, mediengrp, zweigstelle, hstkurz, verfkurz, auslanz):
        if not self.is_valid_mediennr(mediennrex):
            return "Fehler: Die eingegebene Mediennummer ist ungültig."

        exemplarnr = self.generate_exemplarnr()
        if exemplarnr is None:
            return "Exemplarnummer konnte nicht generiert werden."

        try:
            insert_query = """
            INSERT INTO dbo.Exemplar (EXEMPLARNR, ZUGANGSDATUM, MEDIENGRP, ZWEIGSTELLE, 
            AUSLANZJAHR, AUSLANZGES, AUSLANZVORJAHR, AUSLANZVVORJAHR, AUSLANZVVVVORJAHR, 
            HSTKURZ, VERFKURZ, MEDIENNREX, AUSLANZVVVORJAHR)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            # Platzhalter für nicht verwendete Spalten bleiben 0
            auslanzjahr = auslanzges = auslanzvorjahr = auslanzvvorjahr = auslanzvvvorjahr = 0
            self.cursor.execute(insert_query, (exemplarnr, zugangsdatum, mediengrp, zweigstelle, 
                                            auslanzjahr, auslanzges, auslanzvorjahr, auslanzvvorjahr, 
                                            auslanzvvvorjahr, hstkurz, verfkurz, mediennrex, auslanz))
            self.connection.commit()
            return f"Neuer Eintrag in Exemplar mit EXEMPLARNR {exemplarnr} hinzugefügt."
        except Exception as e:
            return f"Fehler beim Hinzufügen des Eintrags in Exemplar: {e}"

    def delete_exemplar(self, exemplarnr):
        if not self.is_valid_exemplarnr(exemplarnr):
            return "Fehler: Die eingegebene Exemplarnummer ist ungültig."

        try:
            delete_query = "DELETE FROM dbo.Exemplar WHERE EXEMPLARNR = ?"
            self.cursor.execute(delete_query, (exemplarnr,))
            self.connection.commit()
            return f"Eintrag in Exemplar mit EXEMPLARNR {exemplarnr} gelöscht."
        except Exception as e:
            return f"Fehler beim Löschen des Eintrags in Exemplar: {e}"

    def update_exemplar(self, exemplarnr, zugangsdatum=None, mediengrp=None, zweigstelle=None, hstkurz=None, verfkurz=None, mediennrex=None):
        if not self.is_valid_exemplarnr(exemplarnr):
            return "Fehler: Die eingegebene Exemplarnummer ist ungültig."
        if mediennrex and not self.is_valid_mediennr(mediennrex):
            return "Fehler: Die eingegebene Mediennummer ist ungültig."

        try:
            update_query = "UPDATE dbo.Exemplar SET "
            params = []
            if zugangsdatum:
                update_query += "ZUGANGSDATUM = ?, "
                params.append(zugangsdatum)
            if mediengrp:
                update_query += "MEDIENGRP = ?, "
                params.append(mediengrp)
            if zweigstelle:
                update_query += "ZWEIGSTELLE = ?, "
                params.append(zweigstelle)
            if hstkurz:
                update_query += "HSTKURZ = ?, "
                params.append(hstkurz)
            if verfkurz:
                update_query += "VERFKURZ = ?, "
                params.append(verfkurz)
            if mediennrex:
                update_query += "MEDIENNREX = ?, "
                params.append(mediennrex)

            update_query = update_query.rstrip(", ") + " WHERE EXEMPLARNR = ?"
            params.append(exemplarnr)

            self.cursor.execute(update_query, params)
            self.connection.commit()
            return f"Eintrag in Exemplar mit EXEMPLARNR {exemplarnr} aktualisiert."
        except Exception as e:
            return f"Fehler beim Bearbeiten des Eintrags in Exemplar: {e}"
