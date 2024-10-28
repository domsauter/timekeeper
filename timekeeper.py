import tkinter as tk
import os
import pandas as pd
from datetime import datetime

def enter_id():
    user_id = id_input.get().strip()
    
    if id_is_correct():
        # Hole die zusätzlichen Informationen aus der Excel-Datei
        name, department = get_user_info(user_id)
        
        # Hole das aktuelle Datum und die aktuelle Zeit
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Schreibe die Informationen in die Logdatei
        try:
            with open('log.txt', 'a') as file:
                file.write(f'{current_datetime} - ID: {user_id}, Name: {name}, Abteilung: {department}\n')
        except IOError as e:
            label.config(text=f"Fehler beim Schreiben in die Logdatei: {str(e)}")
        
        label.config(text="Du bist jetzt eingeloggt.")
    else:
        label.config(text="Das war keine gültige ID.")

def id_is_correct():
    user_id = id_input.get().strip()  # Entfernt führende und nachgestellte Leerzeichen

    try:
        # Excel-Datei einlesen
        df = pd.read_excel('id.xlsx')
        
        # Debugging-Ausgabe der eingelesenen IDs
        print("IDs in der Excel-Datei:", df['ID'].astype(str).tolist())
        
        # Sicherstellen, dass die ID-Spalte als String behandelt wird und Leerzeichen entfernt werden
        df['ID'] = df['ID'].astype(str).str.strip()
        
        return user_id in df['ID'].values
    except FileNotFoundError:
        label.config(text="Fehler: Datei 'id.xlsx' nicht gefunden.")
        return False
    except Exception as e:
        label.config(text=f"Ein Fehler ist aufgetreten: {str(e)}")
        return False

def get_user_info(user_id):
    try:
        # Excel-Datei einlesen
        df = pd.read_excel('id.xlsx')
        
        # Debugging-Ausgabe des gesamten DataFrames
        print("DataFrame aus Excel-Datei:", df)
        
        # Filtere die Zeile mit der angegebenen ID
        user_row = df[df['ID'].astype(str).str.strip() == user_id]
        
        if not user_row.empty:
            name = user_row.iloc[0]['Name']  # Ersetze 'Name' durch den tatsächlichen Namen der Spalte
            department = user_row.iloc[0]['Abteilung']  # Ersetze 'Abteilung' durch den tatsächlichen Namen der Spalte
            return name, department
        else:
            return "Unbekannt", "Unbekannt"
    except FileNotFoundError:
        label.config(text="Fehler: Datei 'id.xlsx' nicht gefunden.")
        return "Fehler", "Fehler"
    except Exception as e:
        label.config(text=f"Ein Fehler ist aufgetreten: {str(e)}")
        return "Fehler", "Fehler"

user = os.getlogin()

app = tk.Tk()
app.title("Timekeeper")

# Setze die Fenstergröße auf 400x300 Pixel
app.geometry("400x300")

label = tk.Label(app, text=f"Hallo {user}, bitte gib Deine Mitarbeiter-ID ein.")
label.pack()

user_id = tk.StringVar()
id_input = tk.Entry(app, textvariable=user_id)
id_input.pack()

button = tk.Button(app, text="Bestätigen", command=enter_id)
button.pack()

app.mainloop()
