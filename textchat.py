import streamlit as st
import netz2v5 as n2  # Importiere das Modul mit den wichtigen Methoden

# Funktion zur Auswahl des aktuellen Fensters (Seite)
def main():
    # Initialisierung des Seitenstatus im session_state
    if 'page' not in st.session_state:
        st.session_state.page = 'main'  # Standardseite ist die Hauptseite
    if 'messages' not in st.session_state:
        st.session_state.messages = []  # Liste für Nachrichten

    # Initialisierung der Dropdowns und anderer Daten, falls noch nicht vorhanden
    if 'geschlecht' not in st.session_state:
        st.session_state.geschlecht = "Keine Angabe"
    if 'alter' not in st.session_state:
        st.session_state.alter = "Keine Angabe"
    if 'buchseiten' not in st.session_state:
        st.session_state.buchseiten = "Keine Angabe"
    if 'fiktive_welt' not in st.session_state:
        st.session_state.fiktive_welt = "Keine Angabe"
    if 'confirmed' not in st.session_state:
        st.session_state.confirmed = False  # Bestätigungsstatus
    if 'dialog' not in st.session_state:
        st.session_state.dialog = ""  # Der Dialog für den Buchvorschlag

    # Seiten basierend auf dem Zustand anzeigen
    if st.session_state.page == 'main':
        show_main_page()
    elif st.session_state.page == 'suggestions':
        show_suggestions_page()
    elif st.session_state.page == 'chat':
        show_chat_page()
    elif st.session_state.page == 'rating':
        show_rating_page()  # Rating Page hinzufügen

# Hauptseite mit den Buttons
def show_main_page():
    # Titel zentral ausrichten
    st.markdown("<h1 style='text-align: center;'>Willkommen zu BiblioMind</h1>", unsafe_allow_html=True)

    # Beschreibung zentriert anzeigen
    st.markdown(
        "<p style='text-align: center;'>BiblioMind hilft dir, die besten Bücher zu finden!</p>", 
        unsafe_allow_html=True
    )

    # Stadtwien Logo oben rechts anzeigen
    st.image("C:/Users/koese/Desktop/FirstStreamlitProjekt/Pictures/stadtwien.png", width=100, use_column_width=False)

    # Zwei Spalten für die nebeneinander liegenden Buttons
    col1, col2 = st.columns([1, 1])  # Gleiche Breite für beide Spalten

    # Button "Buchvorschlag erhalten" in der ersten Spalte
    with col1:
        if st.button('Buchvorschlag erhalten'):
            st.session_state.page = 'suggestions'  # Wechsel zur Seite für die Auswahl der Dropdowns
            st.rerun()  # Seite neu laden

    # Button "Buchvorschlag Bewerten" in der zweiten Spalte
    with col2:
        if st.button('Buchvorschlag bewerten'):
            st.session_state.page = 'rating'  # Wechsel zur Bewertungs-Seite
            st.rerun()  # Seite neu laden

# Seite mit den Dropdown-Listen für die Auswahl der Daten
def show_suggestions_page():
    # Zwei Spalten für die nebeneinander liegenden Buttons
    col1, col2 = st.columns([1, 5])

    # Zurück-Button oben links, vor der Überschrift
    with col1:
        if st.button('← Zurück zur Hauptseite'):
            # Zurücksetzen der session_state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.page = 'main'  # Wechsel zur Hauptseite
            st.rerun()  # Seite neu laden

    # Anzeige des Begrüßungstexts
    st.markdown("<h3 style='text-align: center;'>Willkommen bei BiblioMind!</h3>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center;'>Um dir den bestmöglichen Buchvorschlag geben zu können, möchten wir dir vorab einige vorgefertigte Fragen stellen.</p>",
        unsafe_allow_html=True
    )

    st.title("Buchvorschlag erhalten")

    # Zeigt die Dropdown-Optionen, wenn nicht bestätigt wurde
    if not st.session_state.confirmed:
        # Vier Dropdowns zur Eingabe von Informationen
        col1, col2, col3, col4 = st.columns(4)

        # Geschlecht in der ersten Spalte
        with col1:
            geschlecht = st.selectbox("Geschlecht", ["Keine Angabe", "Männlich", "Weiblich", "Divers"], index=0, key="geschlecht")

        # Alter in der zweiten Spalte
        with col2:
            alter = st.selectbox("Alter", ["Keine Angabe"] + [str(i) for i in range(1, 101)], index=0, key="alter")

        # Buchseiten in der dritten Spalte
        with col3:
            buchseiten = st.selectbox("Anzahl der Buchseiten", ["Keine Angabe", "<150", "150-500", ">500"], index=0, key="buchseiten")

        # Reale oder fiktive Welt in der vierten Spalte
        with col4:
            fiktive_welt = st.selectbox("Reale Welt oder Fiktive Welt", ["Keine Angabe", "Real", "Fiktiv"], index=0, key="fiktive_welt")

        # Bestätigungs-Button anzeigen (grau, wenn nicht alles ausgefüllt ist)
        if st.button("Bestätigen"):
            # Hinzufügen der Angaben als System-Nachricht in die Nachrichten
            st.session_state.messages.append({"role": "System", "text": f"Geschlecht: {geschlecht}"})
            st.session_state.messages.append({"role": "System", "text": f"Alter: {alter}"})
            st.session_state.messages.append({"role": "System", "text": f"Anzahl der Buchseiten: {buchseiten}"})
            st.session_state.messages.append({"role": "System", "text": f"Reale Welt oder Fiktive Welt: {fiktive_welt}"})
            st.session_state.confirmed = True  # Bestätigung speichern

            # Hole Standardfragen und zufällige Fragen
            standard_questions = n2.get_standard_questions()
            random_questions = n2.get_random_questions()

            # Dialog erstellen
            dialog = ""
            for i in range(4):  # Standardfragen hinzufügen
                dialog += f"System: {standard_questions[i]['text']} \n"
                dialog += f"User: {st.session_state[standard_questions[i]['id'].lower()]} \n"
            
            for i in range(3):  # Zufällige Fragen hinzufügen
                dialog += f"System: {random_questions[i]} \n"
                dialog += f"User: Antwort {i+1} \n"
            
            # Buchvorschlag holen und speichern
            buchvorschlag, feedback_code = n2.suggest_book(dialog)
            st.session_state.messages.append({"role": "System", "text": f"Dein Buchvorschlag ist: {buchvorschlag}"})
            st.session_state.messages.append({"role": "System", "text": f"Dein Feedback-Code ist: {feedback_code}"})
            
            # Wechsel zum Chat
            st.session_state.page = 'chat'  # Wechsel zum Chat
            st.rerun()  # Seite neu laden

# Chat-Seite
def show_chat_page():
    # Zwei Spalten für die nebeneinander liegenden Buttons
    col1, col2 = st.columns([1, 5])

    # Zurück-Button oben links, vor der Überschrift
    with col1:
        if st.button('← Zurück zur Hauptseite'):
            # Zurücksetzen der session_state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.page = 'main'  # Wechsel zur Hauptseite
            st.rerun()  # Seite neu laden

    st.title("Buchvorschlag bekommen")

    # Anzeige des Chatverlaufs
    chat_history = ""
    for msg in st.session_state.messages:
        chat_history += f"{msg['role']}: {msg['text']}\n"

    # Textarea für den Chatverlauf
    st.text_area("Chatverlauf", value=chat_history, height=300, max_chars=None, key="chat_history", disabled=True)

    # Eingabefeld für Benutzer
    user_input = st.text_input("Deine Nachricht:", "")

    # Senden-Button
    if st.button("Senden") and user_input:
        # Benutzer-Nachricht hinzufügen
        st.session_state.messages.append({"role": "User", "text": user_input})

        # System-Antwort generieren (hier eine einfache Antwort)
        system_response = get_system_response(user_input)
        st.session_state.messages.append({"role": "System", "text": system_response})

        # Textfeld nach der Nachricht zurücksetzen
        st.session_state.input_text = ""

        # Seite neu laden, um den Chatverlauf anzuzeigen
        st.rerun()  # Seite neu laden mit der Methode st.rerun()

# Funktion, die eine Antwort des Systems generiert
def get_system_response(user_message):
    # Einfache Logik für die Systemantwort
    if "hallo" in user_message.lower():
        return "Hallo! Wie kann ich dir helfen?"
    elif "wie geht es" in user_message.lower():
        return "Mir geht es gut, danke der Nachfrage! Wie geht es dir?"
    else:
        return "Das habe ich leider nicht ganz verstanden. Kannst du es noch einmal versuchen?"

# Bewertungs-Seite für den Buchvorschlag
def show_rating_page():
    # Zwei Spalten für die nebeneinander liegenden Buttons
    col1, col2 = st.columns([1, 5])

    # Zurück-Button oben links, vor der Überschrift
    with col1:
        if st.button('← Zurück zur Hauptseite'):
            # Zurücksetzen der session_state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.page = 'main'  # Wechsel zur Hauptseite
            st.rerun()  # Seite neu laden

    st.title("Buchvorschlag bewerten")

    # Eingabefeld für den Feedback-Code
    zahlencode = st.text_input("Gib den Feedback-Code des Buches ein:", placeholder="z.B. n177x3")

    # Sternebewertung
    st.subheader("Bewerte das Buch (1 bis 5 Sterne):")

    # Sterne: 1 bis 5 Sterne, der Benutzer klickt auf einen Stern
    stars = [1, 2, 3, 4, 5]
    rating = st.radio("Wähle eine Bewertung:", stars, format_func=lambda x: "★" * x)  # Stern-Symbol für jede Zahl anzeigen

    # Button für das Abgeben der Bewertung
    if st.button("Bewertung abgeben"):
        if zahlencode.strip():
            # Fehlerbehandlung für das Speichern der Bewertung
            try:
                n2.save_feedback(zahlencode, rating)
                st.success(f"Du hast das Buch mit {rating} Sternen bewertet.")
            except Exception as e:
                st.error(f"Fehler beim Speichern der Bewertung: {str(e)}")
        else:
            st.error("Bitte gib einen gültigen Feedback-Code ein.")

# Anwendung starten
if __name__ == "__main__":
    main()
