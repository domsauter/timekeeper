import pandas as pd

def get_user_info(user_id, greeting_label):
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
        greeting_label.config(text="Fehler: Datei 'id.xlsx' nicht gefunden.")
        return "Fehler", "Fehler"
    except Exception as e:
        greeting_label.config(text=f"Ein Fehler ist aufgetreten: {str(e)}")
        return "Fehler", "Fehler"