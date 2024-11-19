from datetime import datetime
from ID_Is_Correct import id_is_correct
from Get_User_Info import get_user_info

def enter_id(id_input, message_label, app):
    user_id = id_input.get().strip()
    
    if id_is_correct(user_id, message_label):
        # Hole die zusätzlichen Informationen aus der Excel-Datei
        name, department = get_user_info(user_id, message_label)
        
        # Hole das aktuelle Datum und die aktuelle Zeit
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Schreibe die Informationen in die Logdatei
        try:
            with open('log.txt', 'a') as file:
                file.write(f'{current_datetime} - ID: {user_id}, Name: {name}, Abteilung: {department}\n')
        except IOError as e:
            message_label.config(text=f"Fehler beim Schreiben in die Logdatei: {str(e)}", fg="red")
            return
        
        # Temporäre Nachricht anzeigen
        message_label.config(text="Du bist jetzt eingeloggt.", fg="green")
        app.after(3000, lambda: message_label.config(text=""))  # Nachricht nach 3 Sekunden ausblenden
    else:
        message_label.config(text="Das war keine gültige ID.", fg="red")
        app.after(3000, lambda: message_label.config(text=""))  # Nachricht nach 3 Sekunden ausblenden