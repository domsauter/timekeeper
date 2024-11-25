import tkinter as tk
import os
from Enter_ID import enter_id

user = os.getlogin()

app = tk.Tk()
app.title("Timekeeper")

# Setze die Fenstergröße auf 400x300 Pixel
app.geometry("400x300")

greeting_label = tk.Label(app, text=f"Hallo {user}, bitte gib Deine Mitarbeiter-ID ein.")
greeting_label.pack(pady=10)

user_id = tk.StringVar()
id_input = tk.Entry(app, textvariable=user_id)
id_input.pack()

# Nachricht direkt unter dem Eingabefeld anzeigen
message_label = tk.Label(app, text="", fg="green")  # Nachricht unter Eingabefeld
message_label.pack()

# Funktion, die bei Drücken der Enter-Taste oder des Bestätigen-Buttons aufgerufen wird
def submit_id(event=None):
    enter_id(id_input, message_label, app)
    id_input.delete(0, tk.END)  # Leert das Eingabefeld

# Bind the Enter key to the submit_id function
id_input.bind('<Return>', submit_id)

submit_button = tk.Button(app, text="Einloggen", command=submit_id)
submit_button.pack(pady=10)

#über if-anweisungen Einlogg/Auslogg Button anzeigen 
print(f"input: {id_input}")
#if id_input

app.mainloop()