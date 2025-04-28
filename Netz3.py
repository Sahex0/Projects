import pyodbc
import tensorflow as tf
import numpy as np
from sklearn.preprocessing import StandardScaler
import os
import random

# Setze den Zufalls-Seed für Reproduzierbarkeit
seed = 42
random.seed(seed)
np.random.seed(seed)
tf.random.set_seed(seed)
os.environ['PYTHONHASHSEED'] = str(seed)

# Verbindung zur Datenbank herstellen
connection = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=bibliomind.database.windows.net;'  
    'DATABASE=bibliomind;'      
    'Authentication=ActiveDirectoryInteractive;'
    'UID=sahel.ahmadzai@edu.szu.at;'                
)

# Abfrage für alle relevanten Spalten (Feedback und Fragen)
cursor = connection.cursor()
cursor.execute("""
    SELECT *
    FROM Buchvorschlag_OneHot
""")

# Hole die Spaltennamen (erst die erste Zeile abfragen)
columns = [column[0] for column in cursor.description]

# Finde die Frage-Spalten (die Spalten, die die Zahlen repräsentieren)
frage_columns = [col for col in columns if col.replace('.0', '').isdigit()]
 
# Daten vorbereiten
X = []  # Eingabedaten (Fragen)
y = []  # Zielwerte (Feedback)

# Die Daten auslesen und in X und y umwandeln
for row in cursor.fetchall():
    feedback = row[3]  # Feedback ist die vierte Spalte
    fragen = [row[columns.index(f)] for f in frage_columns]  # Fragen-Spalten extrahieren
    X.append(fragen)
    y.append(feedback)

# Umwandeln in NumPy Arrays
X = np.array(X)
y = np.array(y)

# Normalisieren der Feedback-Werte (falls gewünscht, hier als Beispiel)
y = y / 5.0  # Normalisiert auf den Bereich [0, 1]

# Daten skalieren
scaler = StandardScaler()
X = scaler.fit_transform(X)

# TensorFlow Modell erstellen
model = tf.keras.Sequential([
    tf.keras.layers.InputLayer(input_shape=(X.shape[1],)),  # Eingabeschicht
    tf.keras.layers.Dense(128, activation='relu'),  # Erste versteckte Schicht
    tf.keras.layers.Dropout(0.2),  # Dropout-Schicht
    tf.keras.layers.Dense(64, activation='relu'),  # Zweite versteckte Schicht
    tf.keras.layers.Dropout(0.2),  # Dropout-Schicht
    tf.keras.layers.Dense(32, activation='relu'),  # Dritte versteckte Schicht
    tf.keras.layers.Dense(1)  # Ausgabeschicht, ein Wert für das Feedback
])
  
# Modell kompilieren
model.compile(optimizer='adam', loss='mean_squared_error')

# Modell trainieren
model.fit(X, y, epochs=50, batch_size=16)

# Nach dem Training, die Gewichtung der Eingabeschicht anzeigen
weights = model.layers[0].get_weights()[0]  # Die Gewichte der Eingabeschicht

# Gewichte und zugehörige Fragen sortieren
sorted_weights = sorted(zip(frage_columns, weights), key=lambda x: x[1][0], reverse=True)
# Zeige alle Gewichte der Fragen an
print("\nAlle Gewichte der Fragen (sortiert):")
for weight in sorted_weights:
    print(f"{weight[0]}: {weight[1][0]:.3f}")
# Zeige die 5 besten und 5 schlechtesten Fragen
print("\nTop 5 Fragen:")
for weight in sorted_weights[:5]:
    print(f"{weight[0]}: {weight[1][0]:.3f}")

print("\nBottom 5 Fragen:")
for weight in sorted_weights[-5:]:
    print(f"{weight[0]}: {weight[1][0]:.3f}")

# Vergleiche die aktuellen Gewichte mit den gespeicherten Gewichten
weights_file = 'weights.txt'
if os.path.exists(weights_file):
    with open(weights_file, 'r') as file:
        previous_weights = [float(line.strip()) for line in file.readlines()]
    
    # Berechne die Differenzen zwischen den aktuellen und vorherigen Gewichten
    weight_differences = [(frage_columns[i], weights[i][0] - previous_weights[i]) for i in range(len(weights))]
    
    # Sortiere die Differenzen
    sorted_differences = sorted(weight_differences, key=lambda x: x[1], reverse=True)
    
    print("\nTop 5 positive Differenzen:")
    for diff in sorted_differences[:5]:
        print(f"{diff[0]}: Differenz = {diff[1]:.3f}")
    
    print("\nTop 5 negative Differenzen:")
    for diff in sorted_differences[-5:]:
        print(f"{diff[0]}: Differenz = {diff[1]:.3f}")
else:
    print("\nKeine vorherigen Gewichte gefunden.")

# Speichere die aktuellen Gewichte in einer Textdatei
with open(weights_file, 'w') as file:
    for weight in weights:
        file.write(f"{weight[0]}\n")