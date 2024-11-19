import pandas as pd

def id_is_correct(user_id, message_label):
    try:
        # Excel-Datei einlesen
        df = pd.read_excel('id.xlsx')
        
        # Debugging-Ausgabe der eingelesenen IDs
        print("IDs in der Excel-Datei:", df['ID'].astype(str).tolist())
        
        # Sicherstellen, dass die ID-Spalte als String behandelt wird und Leerzeichen entfernt werden
        df['ID'] = df['ID'].astype(str).str.strip()
        
        return user_id in df['ID'].values
    except FileNotFoundError:
        message_label.config(text="Fehler: Datei 'id.xlsx' nicht gefunden.")
        return False
    except Exception as e:
        message_label.config(text=f"Ein Fehler ist aufgetreten: {str(e)}")
        return False