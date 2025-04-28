import streamlit as st
import netz2v5 as n2
import deniz as d
import Fragen as f

# Initialisiere die Datenbankverbindung
db_handler = d.DatabaseHandler()

# Funktion zur Initialisierung von Session-State-Variablen
def initialize_session_state():
    # Standardwerte für alle session_state-Variablen
    default_values = {
        'page': 'main',
        'messages': [],
        'dialog': "",
        'confirmed': False,
        'is_admin': False,
    }
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value


# Funktion zur Initialisierung von Session-State-Variablen
def initialize_session_state():
    default_values = {
        'page': 'main',
        'messages': [],
        'dialog': "",
        'confirmed': False,
        'is_admin': False,
        'current_question': 0,  # Hinzufügen der fehlenden Variable
    }
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value

def initialize_session_state():
    # Standardwerte für alle session_state-Variablen
    default_values = {
        'page': 'main',
        'messages': [],
        'dialog': "",
        'confirmed': False,
        'is_admin': False,
        'current_question': 0,
        'star_rating': 0,  # Initialisierung von star_rating
    }
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value
            
# Funktion zum Erstellen des Dialogs
def create_dialog(dropdown1, dropdown2, dropdown3, dropdown4, answers):
    """Erstellt einen Dialog basierend auf den Dropdown-Auswahlen und den Antworten auf Systemfragen."""
    standard_questions = n2.get_standard_questions()  # Holt die Standardfragen aus der DB
    random_questions = n2.get_random_questions()  # Holt 3 zufällige Fragen aus der DB
    dialog = ""

    # Standardfragen und deren Antworten
    dialog += f"System: Geschlecht: {dropdown1}\n"
    dialog += f"System: Alter: {dropdown2}\n"
    dialog += f"System: Anzahl der Buchseiten: {dropdown3}\n"
    dialog += f"System: Reale Welt oder Fiktive Welt: {dropdown4}\n"

    # Zufällige Fragen und deren Antworten
    for i in range(3):
        dialog += f"System: {random_questions[i][1]}\n"  # Zufällige Frage
        dialog += f"User: {answers[i]}\n"  # Antwort des Nutzers

    return dialog

# Funktion zur Auswahl des aktuellen Fensters (Seite)
def main():
    # Initialisierung der Session-State-Variablen
    initialize_session_state()

    # Globales Styling (hier den Code einfügen)
    st.markdown(
        """
        <style>
            body {
                background-color: #f5f5f5; /* Sanftes Grau für den Hintergrund */
                font-family: 'Arial', sans-serif; /* Klare Schriftart */
            }
            h1 {
                color: #13468d; /* Dunkelblau */
                font-size: 2.5rem; /* Große Schrift */
                font-weight: bold;
                text-align: center;
                margin-bottom: 30px;
            }
            h2, h3 {
                color: #333333; /* Dunkles Grau */
                text-align: center;
            }
            .center-logo {
                display: block;
                margin: 30px auto; /* Abstand und Zentrierung */
                width: 200px; /* Größe des Logos */
            }
            .stButton button {
                background-color:rgb(127, 185, 224); /* Blau */
                color: #555555; /* Leichter grauer Text */
                font-size: 16px;
                padding: 10px 20px;
                border-radius: 8px; /* Abgerundete Ecken */
                border: none;
                cursor: pointer;
                transition: background-color 0.3s ease, color 0.3s ease; /* Glatter Übergang */
            }

            .stButton button:hover {
                background-color: #2980b9; /* Dunkleres Blau beim Hover */
                color: white; /* Beibehalten der Schriftfarbe */
            }
            .feedback-container {
                background: #ffffff;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                margin: 20px auto;
                max-width: 800px; /* Beschränke die Breite */
            }
            textarea, .stTextInput input {
                font-size: 16px; /* Größerer Eingabetext */
                border-radius: 8px; /* Abgerundete Ecken */
                border: 1px solid #ddd;
                padding: 10px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    # Rest Ihrer main()-Logik
    st.sidebar.markdown("### Admin-Zugang")
    if not st.session_state.is_admin:
        password = st.sidebar.text_input("Passwort eingeben:", type="password")
        if st.sidebar.button("Einloggen"):
            if password == "admin123":  # Beispielpasswort
                st.session_state.is_admin = True
                st.sidebar.success("Erfolgreich eingeloggt!")
            else:
                st.sidebar.error("Falsches Passwort!")
    else:
        st.sidebar.success("Admin angemeldet")
        if st.sidebar.button("Abmelden"):
            st.session_state.is_admin = False
            st.rerun()

    # Seitensteuerung
    if st.session_state.page == 'main':
        show_main_page()
    elif st.session_state.page == 'suggestions':
        show_suggestions_page()
    elif st.session_state.page == 'chat':
        show_chat_page()
    elif st.session_state.page == 'rating':
        show_rating_page()
    elif st.session_state.page == 'admin':
        show_admin_page()

# Funktion zur Anpassung des Admin-Bereich-Buttons
def show_main_page():



    # Styling der gesamten Seite und Buttons
    st.markdown(
        """
        <style>
            body {
                background-color: #f9f9f9; /* Leichte graue Hintergrundfarbe */
            }
            h1 {
                margin-top: -90px; /* Verschiebt den Titel ganz nach oben */
                margin-bottom: -1000px; /* Optional: Abstand nach unten */
                color: rgb(19, 70, 141); /* Dunkelblau */
                font-size: 3rem; /* Größe des Titels */
                font-weight: bold;
                text-align: center;
            }
            body {
                padding-top: 0px; /* Entfernt Standardabstand von oben */
            }
            p {
                margin-top: 0;
                margin-bottom: 0px;
                color: #555555; /* Leichter grauer Text */
                font-size: 1.5rem; /* Vergrößert die Beschreibung */
                text-align: center;
            }
            .center-logo {
                display: block;
                margin-left: auto;
                margin-right: auto;
                margin-bottom: 0px; /* Abstand nach unten */
                width: 500px; /* Vergrößert das Logo */
            }
            .stButton button {
                background-color:rgb(127, 185, 224); /* Blau */
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 15px;
                border: none;
                transition: background-color 0.3s ease, transform 0.2s ease; /* Animation */
            }
            .stButton button:hover {
                background-color: #2980b9; /* Dunkleres Blau beim Hover */
                transform: scale(1.05); /* Leichte Vergrößerung beim Hover */
            }
            .admin-button-container {
                position: fixed;
                bottom: 20px;
                left: 20px;
                z-index: 1000; /* Button bleibt sichtbar */
            }
           
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Titel
    st.markdown("<h1>Willkommen zu BiblioMind</h1>", unsafe_allow_html=True)

    # Beschreibung
    st.markdown(
        "<p>BiblioMind hilft dir, die besten Bücher zu finden!</p>", 
        unsafe_allow_html=True
    )
    
    # Logo zentrieren und vergrößern
    st.markdown(
        """
        <div>
            <img src="https://imgur.com/FdXIZcW.png" class="center-logo" />
        </div>
        """,
        unsafe_allow_html=True
    )

    # Buttons in zwei Spalten zentriert
    col1, col2 = st.columns([1, 1])  # Zwei gleich breite Spalten für die Buttons
    with col1:
        if st.button("Buchvorschlag erhalten", key="suggestion_button"):
            st.session_state.page = "suggestions"  # Navigiere zur Seite für Buchvorschläge
            st.rerun()  # Aktualisiere die Seite
    with col2:
        if st.button("Buchvorschlag bewerten", key="rating_button"):
            st.session_state.page = "rating"  # Navigiere zur Bewertungsseite
            st.rerun()  # Aktualisiere die Seite

    # Admin-Bereich-Button nur für Admins anzeigen
    if st.session_state.is_admin:
        st.markdown('<div class="admin-button-container">', unsafe_allow_html=True)
        if st.button("Admin-Bereich", key="admin_area_button"):
            st.session_state.page = "admin"  # Navigiere zur Admin-Seite
            st.rerun()  # Lade die Seite neu
        st.markdown('</div>', unsafe_allow_html=True)

    # Fügt das GIF unten rechts hinzu
    st.markdown(
        """
        <div style="position: fixed; bottom: 20px; left: 48%; transform: translateX(-50%); text-align: center;">
            <img src="https://static.wixstatic.com/media/e8f830_735ddfa56fd54693a353346621b471b2~mv2.gif" width="500" />
        </div>
        """, 
        unsafe_allow_html=True
)             
    
    # Seite mit den Dropdown-Listen für die Auswahl der Daten
def show_suggestions_page():
    # Styling für Abstand und vertikale Anordnung
    st.markdown(
        """
        <style>
            .content-container {
                margin-top: -10000px; /* Verschiebt den gesamten Inhalt weiter nach oben */
                text-align: center; /* Zentriert den Inhalt */
            }
            .button-container {
                margin-top: 20px; /* Abstand zwischen den Buttons */
                display: flex;
                flex-direction: column; /* Stellt Buttons untereinander */
                align-items: center; /* Zentriert die Buttons */
            }
            .button-container button {
                margin-bottom: 10px; /* Abstand zwischen den Buttons */
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Container für den gesamten Inhalt
    st.markdown('<div class="content-container">', unsafe_allow_html=True)

    # Beschreibung und Titel
    st.markdown(
    """
    <p style="
        text-align: center; 
        font-size: 40px; 
        font-weight: bold;
        font-family: Arial, sans-serif; 
        color:rgb(0, 38, 143); 
        margin-top: -100px; /* Verschiebt den Text nach oben */
        line-height: 1.5;">
        Buchvorschlag Erhalten
    </p>
    """,
    unsafe_allow_html=True
)

    st.markdown(
    """
    <p style="
        text-align: center; 
        font-size: 18px; 
        font-family: Arial, sans-serif; 
        color: #333333; 
        margin-top: -45px; /* Verschiebt den Text nach oben */
        line-height: 1.5;">
        Um dir den bestmöglichen Buchvorschlag geben zu können, möchten wir dir vorab einige vorgefertigte Fragen stellen.
    </p>
    """,
    unsafe_allow_html=True
)

    # Zeigt die Dropdown-Optionen, wenn nicht bestätigt wurde
    if not st.session_state.confirmed:
        # Vier Dropdowns zur Eingabe von Informationen
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.image("https://i.imgur.com/gbnNWk0.png", use_container_width=True)
            geschlecht = st.selectbox("Geschlecht", ["Keine Angabe", "Männlich", "Weiblich", "Divers"], index=0, key="geschlecht")
        with col2:
            st.image("https://i.imgur.com/fAsHJqm.png", use_container_width=True)
            alter = st.selectbox("Alter", ["Keine Angabe"] + [str(i) for i in range(1, 101)], index=0, key="alter")
        with col3:
            st.image("https://i.imgur.com/s1KPdDV.png", use_container_width=True)
            buchseiten = st.selectbox("Anzahl der Buchseiten", ["Keine Angabe", "<150", "150-500", ">500"], index=0, key="buchseiten")
        with col4:
            st.image("https://i.imgur.com/5FKBa2L.png", use_container_width=True)
            fiktive_welt = st.selectbox("Reale Welt oder Fiktive Welt", ["Keine Angabe", "Real", "Fiktiv"], index=0, key="fiktive_welt")

        # Buttons vertikal anordnen
        st.markdown('<div class="button-container">', unsafe_allow_html=True)
        if st.button("Bestätigen", key='confirm_button'):
            # Hinzufügen der Angaben als System-Nachricht in die Nachrichten
            st.session_state.messages.append({"role": "System", "text": f"Geschlecht: {geschlecht}"})
            st.session_state.messages.append({"role": "System", "text": f"Alter: {alter}"})
            st.session_state.messages.append({"role": "System", "text": f"Anzahl der Buchseiten: {buchseiten}"})
            st.session_state.messages.append({"role": "System", "text": f"Reale Welt oder Fiktive Welt: {fiktive_welt}"})
            # Hole die erste zufällige Frage
            q1 = n2.get_random_questions(1)[0][1]
            st.session_state.messages.append({"role": "System", "text": f"{q1}"})
            standard_questions = n2.get_standard_questions()
            st.session_state.dialog = (
                f"System: {standard_questions[0][1]}\n"
                f"User: {geschlecht} \n"
                f"System: {standard_questions[1][1]}\n"
                f"User: {alter} \n"
                f"System: {standard_questions[2][1]}\n"
                f"User: {buchseiten} \n"
                f"System: {standard_questions[3][1]}\n"
                f"User: {fiktive_welt} \n"
                f"System: {q1} \n"
            )
            st.session_state.confirmed = True  # Bestätigung speichern
            st.session_state.page = 'chat'  # Wechsel zum Chat
            st.rerun()  # Seite neu laden

        if st.button("← Zurück zur Hauptseite", key='back_to_main'):
            # Session-State zurücksetzen und zur Hauptseite navigieren
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.page = 'main'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Beende den Container
    st.markdown('</div>', unsafe_allow_html=True)# Chat-Seite

# Chat-Seite mit farbigen Nachrichten und Button-Positionierung
# Chat-Seite
def show_chat_page():
    st.title("Buchvorschlag bekommen")

    # CSS-Styling für die Nachrichtenfarben, Textausrichtung, Hauptfragen und Zentrierung
    st.markdown(
        """
        <style>
        .chat-box {
            font-family: Arial, sans-serif;
            font-size: 16px;
            line-height: 1.6;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 10px;
            background-color: #f9f9f9;
            min-height: 400px; /* Mindesthöhe des Felds */
            max-height: none; /* Keine maximale Höhe */
            overflow-y: visible; /* Scrollen deaktivieren */
        }
        .system-message {
            color: #13468d; /* Dunkelblau für Systemnachrichten */
            text-align: left; /* Links ausgerichtet */
        }
        .user-message {
            color: gray; /* Grau für Benutzernachrichten */
            text-align: right; /* Rechts ausgerichtet */
        }
        .bold-question {
            font-weight: bold; /* Fettgedruckt für die Hauptfragen */
            text-align: center; /* Zentriert */
            display: block; /* Block-Level-Element für korrekte Zentrierung */
        }
        .message {
            margin-bottom: 5px;
            padding: 2px 5px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Anzeige des Chatverlaufs mit farblich markierten Nachrichten und zentrierten Hauptfragen
    chat_history_html = '<div class="chat-box">'
    for msg in st.session_state.messages:
        if msg["role"] == "System" and "Geschlecht" in msg["text"] or \
           msg["role"] == "System" and "Alter" in msg["text"] or \
           msg["role"] == "System" and "Anzahl der Buchseiten" in msg["text"] or \
           msg["role"] == "System" and "Reale Welt oder Fiktive Welt" in msg["text"]:
            role_class = "system-message bold-question"  # Fett und zentriert markieren
        else:
            role_class = "system-message" if msg["role"] == "System" else "user-message"
        chat_history_html += f'<div class="message {role_class}">{msg["text"]}</div>'
    chat_history_html += '</div>'
    st.markdown(chat_history_html, unsafe_allow_html=True)

    # Eingabefeld für Benutzer
    user_input = st.text_input("Deine Nachricht:", "")

    # Zwei Buttons: "Senden" und "Nächste Frage"
    col_send, col_next = st.columns([1, 1])

    with col_send:
        if st.button("Senden", key='send_button') and user_input:
            # Benutzerantwort speichern
            st.session_state.messages.append({"role": "User", "text": user_input})
            st.session_state.dialog += f"User: {user_input} \n"
            st.rerun()  # Seite neu laden, um die Antwort anzuzeigen

    with col_next:
        if st.button("Nächste Frage", key='next_button'):
            # Generiere die nächste zufällige Frage
            qx = n2.get_random_questions(1)[0][1]  # Nächste Frage abrufen
            st.session_state.messages.append({"role": "System", "text": qx})
            st.session_state.dialog += f"System: {qx} \n"
            st.session_state.current_question += 1  # Erhöhe den aktuellen Frage-Index
            st.rerun()  # Seite neu laden, um die neue Frage anzuzeigen

    # Container für die vertikale Button-Anordnung
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    # Button zum Vorschlag bekommen
    if st.button("Vorschlag bekommen", key='get_suggestion_button'):
        # Buchvorschlag generieren
        valid_suggestion, feedback_code = n2.suggest_book(st.session_state.dialog)
        # Ergebnisse anzeigen
        st.write("*Buchvorschlag:*", valid_suggestion)
        st.write("*Feedback-Code:*", feedback_code)

    # Zurück-Button unten
    if st.button("← Zurück zur Hauptseite", key='back_to_main_from_chat'):
        # Zurücksetzen der session_state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.page = 'main'  # Wechsel zur Hauptseite
        st.rerun()  # Seite neu laden
    st.markdown('</div>', unsafe_allow_html=True)
        



# Bewertungs-Seite für den Buchvorschlag

def show_rating_page():
    # Initialisieren Sie den Zustand, falls noch nicht geschehen
    if "star_rating" not in st.session_state:
        st.session_state.star_rating = 0

    # CSS für ein schönes Sterne-System
    st.markdown(
        """
        <style>
        .rating-container {
            text-align: center;
            margin-top: 20px;
            margin-bottom: 30px;
        }
        .star {
            display: inline-block;
            font-size: 3rem;
            cursor: pointer;
            color: lightgray;
            transition: transform 0.2s, color 0.2s;
        }
        .star:hover, .star:hover ~ .star {
            transform: scale(1.2);
            color: #FFD700; /* Gold */
        }
        .star.selected {
            color: #FFD700; /* Gold für ausgewählte Sterne */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Überschrift
    st.markdown('<h1 style="text-align: center; color: #13468d;">Buchvorschlag bewerten</h1>', unsafe_allow_html=True)

    # Eingabefeld für Feedback-Code
    feedback_code = st.text_input("Gib den Feedback-Code des Buches ein:", placeholder="z.B. n177x3")

    # Sterne-Bewertung mit Buttons
    st.markdown('<h3 style="text-align: center;">Bewerte das Buch:</h3>', unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Buttons für Sterne
    with col1:
        if st.button("★", key="star_1"):
            st.session_state.star_rating = 1
    with col2:
        if st.button("★ ★", key="star_2"):
            st.session_state.star_rating = 2
    with col3:
        if st.button("★ ★ ★", key="star_3"):
            st.session_state.star_rating = 3
    with col4:
        if st.button("★ ★ ★ ★", key="star_4"):
            st.session_state.star_rating = 4
    with col5:
        if st.button("★ ★ ★ ★ ★", key="star_5"):
            st.session_state.star_rating = 5

    # Aktuelle Bewertung anzeigen
    st.markdown(
        f'<h4 style="text-align: center;">Aktuelle Bewertung: {"★" * st.session_state.star_rating}</h4>',
        unsafe_allow_html=True,
    )

    # Kommentar-Bereich
    st.markdown('<h3 style="text-align: center;">Dein Kommentar:</h3>', unsafe_allow_html=True)
    comment = st.text_area("", placeholder="Was hat dir gefallen oder nicht gefallen?", key="rating_comment")

    # Absenden-Button
    if st.button("Bewertung absenden"):
        if not feedback_code:
            st.error("Bitte gib den Feedback-Code ein!")
        else:
            st.success(f"Deine Bewertung ({st.session_state.star_rating} Sterne) wurde gespeichert!")
            st.write(f"Kommentar: {comment if comment else 'Kein Kommentar'}")
            st.write(f"Feedback-Code: {feedback_code}")

    # Zur Hauptseite-Button
    if st.button("← Zur Hauptseite"):
        st.session_state.page = "main" 
        st.rerun()  # Seite neu laden, um zur Hauptseite zu navigieren

def show_admin_page():
    st.title("Admin-Bereich")
    st.write("Hier können Sie Einträge verwalten.")

       # Initialisierung von Flags in `st.session_state`, falls sie noch nicht existieren
    if "admin_action" not in st.session_state:
        st.session_state.admin_action = None  # Speichert die aktuelle Aktion
        st.session_state.current_item_id = None  # Speichert die ID für Aktionen (Mediennummer oder Exemplarnummer)

    # Buttons für die Aktionen
    if st.button("Eintrag in Medien hinzufügen"):
        st.session_state.admin_action = "add_media"

    if st.button("Eintrag in Medien löschen"):
        st.session_state.admin_action = "delete_media"

    if st.button("Eintrag in Medien bearbeiten"):
        st.session_state.admin_action = "edit_media"

    if st.button("Eintrag in Exemplare hinzufügen"):
        st.session_state.admin_action = "add_exemplar"

    if st.button("Eintrag in Exemplare löschen"):
        st.session_state.admin_action = "delete_exemplar"

    if st.button("Eintrag in Exemplare bearbeiten"):
        st.session_state.admin_action = "edit_exemplar"



    if st.button("Fragen automatisch hinzufügen"):
        st.session_state.admin_action = "add_auto_questions"

    if st.button("Fragen manuell hinzufügen"):
        st.session_state.admin_action = "add_manual_question"

    if st.button("Fragen bearbeiten"):
        st.session_state.admin_action = "edit_question"

    if st.button("Fragen löschen"):
        st.session_state.admin_action = "delete_question"

    # Je nach gewählter Aktion die Eingabefelder anzeigen
    if st.session_state.admin_action == "add_auto_questions":
        st.write("Automatisch generierte Fragen hinzufügen:")
        num_questions = st.number_input("Anzahl der Fragen", min_value=1, max_value=20, value=5, step=1)
        if st.button("Fragen generieren"):
            try:
                added_questions = f.add_auto_questions(num_questions)
                if added_questions:
                    st.success(f"Es wurden {len(added_questions)} neue Fragen hinzugefügt.")
                    st.write("Neue Fragen:", ", ".join(added_questions))
                else:
                    st.warning("Keine neuen Fragen wurden hinzugefügt. Möglicherweise sind alle generierten Fragen bereits vorhanden.")
            except Exception as e:
                st.error(f"Fehler beim Hinzufügen: {e}")

    elif st.session_state.admin_action == "add_manual_question":
        st.write("Manuelle Frage hinzufügen:")
        manual_frage = st.text_input("Neue Frage", placeholder="Geben Sie eine Frage ein")
        if st.button("Frage hinzufügen"):
            try:
                new_id = f.add_manual_question(manual_frage)
                st.success(f"Die Frage wurde erfolgreich hinzugefügt mit der ID {new_id}.")
            except Exception as e:
                st.error(f"Fehler: {e}")

    elif st.session_state.admin_action == "edit_question":
        st.write("Frage bearbeiten:")
        frage_id = st.number_input("Frage-ID", min_value=1, step=1)
        neue_frage = st.text_input("Neue Frage", placeholder="Geben Sie die aktualisierte Frage ein")
        if st.button("Frage aktualisieren"):
            try:
                f.edit_question(frage_id, neue_frage)
                st.success(f"Die Frage mit der ID {frage_id} wurde erfolgreich aktualisiert.")
            except Exception as e:
                st.error(f"Fehler: {e}")

    elif st.session_state.admin_action == "delete_question":
        st.write("Frage löschen:")
        frage_id = st.number_input("Frage-ID", min_value=1, step=1)
        if st.button("Frage löschen"):
            try:
                f.delete_question(frage_id)
                st.success(f"Die Frage mit der ID {frage_id} wurde erfolgreich gelöscht.")
            except Exception as e:
                st.error(f"Fehler: {e}")

    # Je nach gewählter Aktion die Eingabefelder anzeigen
    if st.session_state.admin_action == "add_media":
        st.write("Fügen Sie neue Medien hinzu:")
        col1, col2 = st.columns(2)
        with col1:
            art = st.text_input("Art", placeholder="z.B. Buch")
            verf1 = st.text_input("Verfasser", placeholder="z.B. Max Mustermann")
            hst = st.text_input("Herausgeber", placeholder="z.B. Verlag XYZ")
            syst = st.text_input("Systematik", placeholder="z.B. Belletristik")
        with col2:
            mediengrp = st.text_input("Mediengruppe", placeholder="z.B. Roman")
            jahr = st.text_input("Jahr", placeholder="z.B. 2023")
            isbn = st.text_input("ISBN", placeholder="z.B. 978-3-16-148410-0")
        if st.button("Hinzufügen"):
            if all([art, verf1, hst, syst, mediengrp, jahr, isbn]):
                result = db_handler.add_medien(art, verf1, hst, syst, mediengrp, jahr, isbn)
                st.success(result)
            else:
                st.error("Bitte füllen Sie alle Felder aus!")

    elif st.session_state.admin_action == "delete_media":
        st.write("Löschen Sie Medien:")
        mediennr = st.text_input("Mediennummer", placeholder="z.B. 1234")
        if st.button("Löschen"):
            if mediennr.isdigit():
                result = db_handler.delete_medien(int(mediennr))
                st.success(result)
            else:
                st.error("Bitte geben Sie eine gültige Mediennummer ein.")

    elif st.session_state.admin_action == "edit_media":
        st.write("Bearbeiten Sie Medien:")
        mediennr = st.text_input("Mediennummer", placeholder="z.B. 1234")
        if mediennr and mediennr.isdigit():
            st.session_state.current_item_id = mediennr
            st.session_state.admin_action = "edit_media_form"
        if st.session_state.admin_action == "edit_media_form":
            st.write(f"Bearbeiten Sie die Informationen für Mediennummer {st.session_state.current_item_id}:")
            col1, col2 = st.columns(2)
            with col1:
                art = st.text_input("Neue Art (optional)", placeholder="z.B. Buch")
                verf1 = st.text_input("Neuer Verfasser (optional)", placeholder="z.B. Max Mustermann")
                hst = st.text_input("Neuer Herausgeber (optional)", placeholder="z.B. Verlag XYZ")
                syst = st.text_input("Neue Systematik (optional)", placeholder="z.B. Belletristik")
            with col2:
                mediengrp = st.text_input("Neue Mediengruppe (optional)", placeholder="z.B. Roman")
                jahr = st.text_input("Neues Jahr (optional)", placeholder="z.B. 2023")
                isbn = st.text_input("Neue ISBN (optional)", placeholder="z.B. 978-3-16-148410-0")
            if st.button("Aktualisieren"):
                result = db_handler.update_medien(
                    int(st.session_state.current_item_id),
                    art=art if art.strip() else None,
                    verf1=verf1 if verf1.strip() else None,
                    hst=hst if hst.strip() else None,
                    syst=syst if syst.strip() else None,
                    mediengrp=mediengrp if mediengrp.strip() else None,
                    jahr=jahr if jahr.strip() else None,
                    isbn=isbn if isbn.strip() else None,
                )
                st.success(f"Mediennummer {st.session_state.current_item_id} wurde aktualisiert!")

    elif st.session_state.admin_action == "add_exemplar":
        st.write("Fügen Sie ein neues Exemplar hinzu:")
        col1, col2 = st.columns(2)
        with col1:
            mediennrex = st.text_input("Mediennummer", placeholder="z.B. 1234")
            zugangsdatum = st.date_input("Zugangsdatum", help="Wählen Sie das Zugangsdatum aus")
            mediengrp = st.text_input("Mediengruppe", placeholder="z.B. Roman")
            zweigstelle = st.text_input("Zweigstelle", placeholder="z.B. Hauptbibliothek")
        with col2:
            hstkurz = st.text_input("Herausgeber (Kurzform)", placeholder="z.B. Verlag XYZ")
            verfkurz = st.text_input("Verfasser (Kurzform)", placeholder="z.B. M. Mustermann")
            auslanz = st.text_input("AUSLANZVVVORJAHR", placeholder="z.B. 0")  # Hinzufügen der neuen Eingabe
        
        # Hinzufügen-Button und Validierung
        if st.button("Hinzufügen"):
            # Überprüfen, ob alle Felder ausgefüllt und valide sind
            if mediennrex.isdigit() and mediengrp and zweigstelle and hstkurz and verfkurz and auslanz.isdigit():
                # Funktion aufrufen, mit dem zusätzlichen `auslanz`-Parameter
                result = db_handler.add_exemplar(
                    int(mediennrex),
                    zugangsdatum,
                    mediengrp,
                    zweigstelle,
                    hstkurz,
                    verfkurz,
                    int(auslanz)  # Übergeben des neuen Parameters
                )
                st.success(result)
            else:
                st.error("Bitte füllen Sie alle Felder aus!")

    elif st.session_state.admin_action == "delete_exemplar":
        st.write("Löschen Sie ein Exemplar:")
        exemplarnr = st.text_input("Exemplarnummer", placeholder="z.B. 1234")
        if st.button("Löschen"):
            if exemplarnr.isdigit():
                result = db_handler.delete_exemplar(int(exemplarnr))
                st.success(result)
            else:
                st.error("Bitte geben Sie eine gültige Exemplarnummer ein.")


     # Je nach gewählter Aktion die Eingabefelder anzeigen
    if st.session_state.admin_action == "edit_exemplar":
        st.write("Bearbeiten Sie ein Exemplar:")
        exemplarnr = st.text_input("Exemplarnummer", placeholder="z.B. 1234", key="edit_exemplar_nr")

        # Speichern der eingegebenen Exemplarnummer und Anzeige des Bearbeitungsformulars
        if exemplarnr and exemplarnr.isdigit():
            st.session_state.current_item_id = exemplarnr
            st.session_state.admin_action = "edit_exemplar_form"

    # Bearbeitungsformular für Exemplar anzeigen, wenn eine gültige Nummer eingegeben wurde
    if st.session_state.admin_action == "edit_exemplar_form" and st.session_state.current_item_id:
        st.write(f"Bearbeiten Sie die Informationen für Exemplarnummer {st.session_state.current_item_id}:")
        col1, col2 = st.columns(2)
        with col1:
            zugangsdatum = st.date_input("Neues Zugangsdatum (optional)", key="edit_exemplar_date")
            mediengrp = st.text_input("Neue Mediengruppe (optional)", placeholder="z.B. Roman", key="edit_exemplar_mediengrp")
            zweigstelle = st.text_input("Neue Zweigstelle (optional)", placeholder="z.B. Hauptbibliothek", key="edit_exemplar_branch")
        with col2:
            hstkurz = st.text_input("Neuer Herausgeber (Kurzform, optional)", placeholder="z.B. Verlag XYZ", key="edit_exemplar_hstkurz")
            verfkurz = st.text_input("Neuer Verfasser (Kurzform, optional)", placeholder="z.B. M. Mustermann", key="edit_exemplar_verfkurz")
            mediennrex = st.text_input("Neue Mediennummer (optional)", placeholder="z.B. 1234", key="edit_exemplar_mediennrex")
        
        if st.button("Aktualisieren"):
            result = db_handler.update_exemplar(
                int(st.session_state.current_item_id),
                zugangsdatum=zugangsdatum,
                mediengrp=mediengrp if mediengrp.strip() else None,
                zweigstelle=zweigstelle if zweigstelle.strip() else None,
                hstkurz=hstkurz if hstkurz.strip() else None,
                verfkurz=verfkurz if verfkurz.strip() else None,
                mediennrex=int(mediennrex) if mediennrex.strip() else None,
            )
            st.success(f"Exemplar {st.session_state.current_item_id} wurde aktualisiert!")
            st.session_state.admin_action = None
            st.session_state.current_item_id = None
    
    # Zurück zur Hauptseite
    if st.button("Zurück zur Hauptseite"):
        st.session_state.page = "main"
        st.rerun()

        st.markdown(
    """
    <div style="position: fixed; bottom: 20px; left: 20px; z-index: 1000;">
        <img src="https://play-lh.googleusercontent.com/1lXS_bGAlWWV0-LVNM1yO4H3bYy0JgXrGR2-PzBxDCCdFtoI0pytFHf2hobn4qn7Ofd7" alt="Stadt Wien Logo" width="100">
    </div>
    """,
    unsafe_allow_html=True
)

# Startpunkt der Anwendung
if __name__ == "__main__":
    main()
