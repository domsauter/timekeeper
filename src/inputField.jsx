import React, { useState } from 'react';

function InputField() {
    const [inputValue, setInputValue] = useState(''); // Zustand für den Text im Eingabefeld

    const handleInputChange = (event) => {
        setInputValue(event.target.value); // Aktualisiert den Zustand, wenn sich der Eingabewert ändert
    };

    const handleSaveToFile = () => {
        const blob = new Blob([inputValue], { type: 'text/plain' }); // Erstellt ein Blob-Objekt mit dem eingegebenen Text
        const url = window.URL.createObjectURL(blob); // Erstellt eine URL für das Blob-Objekt
        const a = document.createElement('a'); // Erstellt ein unsichtbares <a>-Element
        a.href = url;
        a.download = 'textdatei.txt'; // Der Dateiname der heruntergeladenen Datei
        a.click(); // Simuliert einen Klick auf den Download-Link
        window.URL.revokeObjectURL(url); // Gibt die Blob-URL frei, um Speicher zu sparen
    };

    return (
        <div>
            <input 
                type="text" 
                value={inputValue} 
                onChange={handleInputChange} 
                placeholder="Gib hier deinen Text ein" 
            />
            <button onClick={handleSaveToFile}>ID-Scan</button> {/* Button, der den Text speichert */}
        </div>
    );
}

export default InputField;
