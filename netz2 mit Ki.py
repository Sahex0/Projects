# Sprint 4 (finales Konsoleprogramm)
import random
import string
import google.generativeai as genai
import pyodbc
import os
from ollama import generate
import time
import datetime


# API Key für LLM
genai.configure(api_key="AIzaSyDA2_bBa9HWJhXBpopoe730dl0ZhdwsOtM")  

# Verbindung zu SQL Server herstellen
connection = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=bibliomind.database.windows.net;'  
    'DATABASE=bibliomind;'      
    'Authentication=ActiveDirectoryInteractive;'
    'UID=sahel.ahmadzai@edu.szu.at;'
)

cursor = connection.cursor()

# Fragen aus der DB
cursor.execute("SELECT Frage_ID, Frage FROM Frage")
fragen_liste = cursor.fetchall() 

# Bücher aus der DB der Bibliothek Wien (Autor und Titel)
cursor.execute("SELECT CAST(HST AS NVARCHAR(MAX)), CAST(VERF1 AS NVARCHAR(MAX)), MEDIENNR FROM MEDIEN")
buecher_liste = []
for row in cursor.fetchall():
    buecher_liste.append({"Titel": row[0], "Autor": row[1], "MEDIENNR": row[2]})

def ExecuteDialog():
    dialog = ""
    antworten_ids = []
    kontext = """
        Du übernimmst zufällig eine neue Identität. Dein Alter ist zwischen 14 und 85 Jahren. 
        Du hast einen beliebigen Hintergrund, Geschlecht und Persönlichkeit. Sei kreativ, aber realistisch.

        Du befindest dich in einer Bibliothek und möchtest ein Buch ausleihen, weißt aber nicht, welches. 
        Dir werden exakt 7 Fragen gestellt. Deine Aufgabe ist es, jede Frage in einem einzigen Satz mit 3 bis 8 Wörtern zu beantworten.

        - Deine Antworten müssen variieren und dürfen keine Muster erkennen lassen.
        - Erwähne niemals, dass du ein Sprachmodell bist.
        - Stelle keine Gegenfragen oder Vermutungen über den Buchvorschlag an.
        - Imitiere nicht das System und erfinde keine zusätzlichen Schritte.
        - Nachdem dir ein Buch vorgeschlagen wurde, gibst du eine Bewertung von 1 bis 5 ab.

        Bleibe in deiner Rolle und folge strikt diesen Regeln. Deine Antworten sollen sich natürlich und menschlich anfühlen.
        """
    dialog += kontext

    cursor.execute("SELECT ISNULL(MAX(Antwort_ID), 0) FROM Antwort")
    max_id = cursor.fetchone()[0]
    next_id = max_id + 1  

    # Standardfragen (ID 1-4)
    standardfragen = [frage for frage in fragen_liste if frage[0] in [1, 2, 3, 4]]
    for frage in standardfragen:
        question_text = frage[1]
        print(f"System: {question_text}")
        dialog += f"System: {question_text}\n"

        response = generate(
            model="llama3.1",
            prompt=dialog,
        )

        antwort = response['response'].strip()
        dialog += f"[Antwort]: {antwort}\n"
        print(f"Llama: {antwort}")

        antworten_ids.append((next_id, antwort, frage[0]))
        next_id += 1

    # 3 zufällige Fragen
    randomfragen = [frage for frage in fragen_liste if frage[0] > 4]
    for _ in range(3):
        frage = random.choice(randomfragen)
        question_text = frage[1]
        print(f"System: {question_text}")
        dialog += f"System: {question_text}\n"

        response = generate(
            model="llama3.1",
            prompt=dialog,
        )

        antwort = response['response'].strip()
        dialog += f"[Antwort]: {antwort}\n"
        print(f"Llama: {antwort}")

        antworten_ids.append((next_id, antwort, frage[0]))
        next_id += 1

    return dialog, antworten_ids

def SuggestBook(dialog):
    model = genai.GenerativeModel("gemini-1.5-pro")
    prompt = (
        "Schlage mir 10 Bücher (ohne Nummerierung) mit den Autor des Buches (in genau diesen Format Nachname, Vorname:Titel wie z.B Schnitzler, Arthur:Medizinische Vorschriften) vor anhand des Dialogs am Ende. "
        "Es dürfen keine weiteren Informationen mehr vergeben werden. Auch wenn Sie denken, dass es unmöglich ist, anhand dieses Dialogs ein Buch vorzuschlagen, machen Sie es trotzdem. "
        "Ich akzeptiere keine andere Antwort.: " + dialog
    )

    response = model.generate_content(prompt)
    buchvorschlaege = response.text.strip().splitlines()  

    valid_suggestion = None  
    invalid_suggestions = []   

    for buchvorschlag in buchvorschlaege:
        autor, *titel = buchvorschlag.split(":") 
        titel = ":".join(titel)
        autor, titel = autor.strip(), titel.strip()

        mediennr = FindBookByTitleAndAuthor(titel, autor)
        
        if mediennr and not valid_suggestion:
            valid_suggestion = (mediennr, titel, autor)
            print(f"System: Gültiges Buch gefunden: {buchvorschlag}")
        elif not mediennr:
            # Ungültigen Vorschlag zur Liste hinzufügen, mit Autor im Titel
            buch_titel = f"{autor}:{titel}"
            invalid_suggestions.append((None, buch_titel, autor))

    return invalid_suggestions, valid_suggestion # wenn Feedback_Code und MEDIENNR null ist, dann weiß man, dass kein Buch in der Bibliothek gefunden wurde

def SuggestBook(dialog):
    model = genai.GenerativeModel("gemini-1.5-pro")
    prompt = (
        "Schlage mir 10 Bücher (ohne Nummerierung) mit den Autor des Buches (in genau diesen Format Nachname, Vorname:Titel wie z.B Schnitzler, Arthur:Medizinische Vorschriften) vor anhand des Dialogs am Ende. "
        "Es dürfen keine weiteren Informationen mehr vergeben werden. Auch wenn Sie denken, dass es unmöglich ist, anhand dieses Dialogs ein Buch vorzuschlagen, machen Sie es trotzdem. "
        "Ich akzeptiere keine andere Antwort.: " + dialog
    )

    response = model.generate_content(prompt)
    buchvorschlaege = response.text.strip().splitlines()  

    valid_suggestion = None  
    invalid_suggestions = []   

    for buchvorschlag in buchvorschlaege:
        autor, *titel = buchvorschlag.split(":") 
        titel = ":".join(titel)
        autor, titel = autor.strip(), titel.strip()

        mediennr = FindBookByTitleAndAuthor(titel, autor)
        
        if mediennr and not valid_suggestion:
            valid_suggestion = (mediennr, titel, autor)
            print(f"System: Gültiges Buch gefunden: {buchvorschlag}")
        elif not mediennr:
            # Ungültigen Vorschlag zur Liste hinzufügen, mit Autor im Titel
            buch_titel = f"{autor}:{titel}"
            invalid_suggestions.append((None, buch_titel, autor))

    return invalid_suggestions, valid_suggestion # wenn Feedback_Code und MEDIENNR null ist, dann weiß man, dass kein Buch in der Bibliothek gefunden wurde


def FindBookByTitleAndAuthor(titel, autor):
    for buch in buecher_liste:
        if buch["Titel"] == titel and buch["Autor"] == autor:
            return buch["MEDIENNR"]
    return None

def generate_feedback_code(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def save_book_recommendation(mediennr, title, feedback_code):
    cursor.execute("SELECT ISNULL(MAX(Buchvorschlag_ID), 0) FROM Buchvorschlag")
    max_id = cursor.fetchone()[0]
    next_id = max_id + 1
    
    cursor.execute(
        "INSERT INTO Buchvorschlag (Buchvorschlag_ID, MEDIENNR, Titel, Feedback, Feedback_Code) VALUES (?, ?, ?, NULL, ?)",
        (next_id, mediennr, title, feedback_code)
    )
    
    return next_id

def save_feedback(feedback_code, rating):
    cursor.execute("UPDATE Buchvorschlag SET Feedback = ? WHERE Feedback_Code = ?", (rating, feedback_code))
    connection.commit()


def main():
    for _ in range(100):
        i=0
        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=bibliomind.database.windows.net;'  
            'DATABASE=bibliomind;'      
            'Authentication=ActiveDirectoryInteractive;'
            'UID=sahel.ahmadzai@edu.szu.at;'
        )

        cursor = connection.cursor()

        # Fragen aus der DB
        cursor.execute("SELECT Frage_ID, Frage FROM Frage")
        fragen_liste = cursor.fetchall() 

        # Bücher aus der DB der Bibliothek Wien (Autor und Titel)
        cursor.execute("SELECT CAST(HST AS NVARCHAR(MAX)), CAST(VERF1 AS NVARCHAR(MAX)), MEDIENNR FROM MEDIEN")
        buecher_liste = []
        for row in cursor.fetchall():
            buecher_liste.append({"Titel": row[0], "Autor": row[1], "MEDIENNR": row[2]})

        dialog, antworten_ids = ExecuteDialog()
        
        invalid_suggestions, valid_suggestion = SuggestBook(dialog)

        feedback_code = generate_feedback_code()
        if valid_suggestion:
            mediennr, titel, autor = valid_suggestion
            recommendation_id = save_book_recommendation(mediennr, titel, feedback_code)
        else:
            recommendation_id = None 

        for (answer_id, answer_text, question_id) in antworten_ids:
            cursor.execute(
                "INSERT INTO Antwort (Antwort_ID, Antwort, Frage_ID, Buchvorschlag_ID) VALUES (?, ?, ?, ?)",
                (answer_id, answer_text, question_id, recommendation_id)
            )

        for mediennr, titel, autor in invalid_suggestions:
            save_book_recommendation(mediennr, titel, None)

        randomNumb = [1,2,3,4,5]
        save_feedback(feedback_code, random.choice(randomNumb))
        connection.commit()


        print("Buchvorschläge und Antworten wurden erfolgreich in der Datenbank gespeichert.")
        dialog = "",
        print(i+1)
        cursor.close()
        connection.close()
        

if __name__ == "__main__":
    main()
