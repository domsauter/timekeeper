import tkinter as tk
import pandas as pd
import logging
from datetime import datetime

# Farbvariablen definieren
BACKGROUND_COLOR = "#191e2b"
SECOND_COLOR = "#46b82e"
SECOND_COLOR_HOVER = "#3d9f28"
TEXT_COLOR = "white"
ERROR_COLOR = "red"

# Log-Konfiguration für Datei und Konsole
logging.basicConfig(
    format='%(asctime)s - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('log.txt'),  # Log in Datei speichern
        logging.StreamHandler()           # Auch in der Konsole ausgeben
    ]
)

def extract_data_from_excel(file_path):
    """Liest die Excel-Datei aus und extrahiert die Zuordnung von IDs zu Mitarbeitern und Stationen."""
    excel_data = pd.ExcelFile(file_path)
    sheet_data = excel_data.parse('Tabelle1')

    # Relevante Spalten bestimmen
    station_columns = ['qualifizierte Stationen', 'Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8']

    # Daten sammeln
    employee_data = {}
    for _, row in sheet_data.iterrows():
        employee_id = row['ID']
        employee_name = row['Name']
        department = row['Abteilung']  # Abteilung hinzufügen
        main_station = row['Hauptstation']
        stations = row[station_columns].dropna().tolist()
        stations.insert(0, main_station)  # Hauptstation hinzufügen

        # Den employee_id als Schlüssel speichern
        employee_data[employee_id] = {
            'id': employee_id,  # ID jetzt als Teil der Datenstruktur
            'name': employee_name,
            'department': department,  # Abteilung speichern
            'stations': stations,
            'current_station': main_station
        }

    return employee_data

def log_station_change(employee_id, employee_name, department, current_station, new_station):
    """Schreibt die Änderungen in die Log-Datei."""
    log_message = f"ID: {employee_id}, Name: {employee_name}, Abteilung: {department}, " \
                  f"Aktuelle Station: {current_station}, Neue Station: {new_station}"
    logging.info(log_message)  # Log-Nachricht wird sowohl in die Datei als auch auf die Konsole geschrieben

def display_main_menu(root, data):
    """Zeigt das Hauptmenü mit der ID-Eingabe an."""
    for widget in root.winfo_children():
        widget.destroy()
    create_id_input(root, data)

def update_current_station(employee, new_station):
    """Aktualisiert die aktuelle Station des Mitarbeiters und loggt die Änderung."""
    current_station = employee['current_station']
    log_station_change(employee['id'], employee['name'], employee['department'], current_station, new_station)  # Loggen
    employee['current_station'] = new_station

def display_employee_buttons(root, employee, data):
    """Zeigt Buttons für die Stationen eines Mitarbeiters an und ermöglicht die Rückkehr zum Hauptmenü."""
    for widget in root.winfo_children():
        widget.destroy()

    label = tk.Label(root, text=f"Mitarbeiter: {employee['name']}", font=("Verdana", 16), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
    label.pack(pady=10)

    current_station_label = tk.Label(root, text=f"Aktuelle Station: {employee['current_station']}", font=("Verdana", 12), fg=SECOND_COLOR, bg=BACKGROUND_COLOR)
    current_station_label.pack(pady=5)

    def on_station_click(station):
        update_current_station(employee, station)
        display_employee_buttons(root, employee, data)

    for station in employee['stations']:
        if station != employee['current_station']:
            button = tk.Button(root, text=station, command=lambda s=station: on_station_click(s), bg=TEXT_COLOR, fg=BACKGROUND_COLOR, font=("Verdana", 10))
            button.pack(pady=5)

    back_button = tk.Button(root, text="Zurück", command=lambda: display_main_menu(root, data), bg=SECOND_COLOR, fg=BACKGROUND_COLOR, font=("Verdana", 10))
    back_button.pack(pady=20)

def on_id_submit(entry, data, root):
    """Verarbeitet die eingegebene ID und zeigt die zugehörigen Buttons an."""
    entered_id = entry.get()
    if entered_id.isdigit() and int(entered_id) in data:
        display_employee_buttons(root, data[int(entered_id)], data)
    else:
        for widget in root.winfo_children():
            widget.destroy()
        label = tk.Label(root, text="Ungültige ID. Bitte erneut versuchen.", fg=ERROR_COLOR, bg=BACKGROUND_COLOR, font=("Verdana", 10))
        label.pack(pady=10)
        back_button = tk.Button(root, text="Zurück", command=lambda: display_main_menu(root, data), bg=SECOND_COLOR, fg=BACKGROUND_COLOR, font=("Verdana", 10))
        back_button.pack(pady=10)

def create_id_input(root, data):
    """Erstellt ein Eingabefeld zur Eingabe der ID."""
    frame = tk.Frame(root, bg=BACKGROUND_COLOR)
    frame.pack(pady=20)

    label = tk.Label(frame, text="Bitte ID eingeben:", font=("Verdana", 10), bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
    label.pack(side="left", padx=5)

    entry = tk.Entry(frame, font=("Verdana", 10))
    entry.pack(side="left", padx=5)

    button = tk.Button(frame, text="Suchen", command=lambda: on_id_submit(entry, data, root), bg=SECOND_COLOR, fg=BACKGROUND_COLOR, font=("Verdana", 10))
    button.pack(side="left", padx=5)

# Tkinter-Fenster erstellen
root = tk.Tk()
root.title("Mitarbeiter und Stationen")

# Hintergrundfarbe setzen
root.configure(bg=BACKGROUND_COLOR)

# Fenstergröße anpassen
root.geometry("800x600")

# Mitarbeiter-Station-Zuordnung aus Excel extrahieren
data = extract_data_from_excel('id.xlsx')

# Hauptmenü anzeigen
display_main_menu(root, data)

# Tkinter-Event-Loop starten
root.mainloop()
