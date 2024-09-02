import React, { useState } from 'react';

function InputField() {
    const [inputValue, setInputValue] = useState(''); // Zustand für den Text im Eingabefeld

    const handleInputChange = (event) => {
        setInputValue(event.target.value); // Aktualisiert den Zustand, wenn sich der Eingabewert ändert
    };

    const handleScanID = async () => {
        try {
            const response = await fetch('http://localhost:3001/scan-id', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ id: inputValue }),
            });

            const result = await response.json();
            if (result.success) {
                alert('ID gefunden und in die Log-Datei geschrieben.');
            } else {
                alert('ID nicht gefunden.');
            }
        } catch (error) {
            console.error('Fehler beim Scannen der ID:', error);
            alert('Es gab einen Fehler beim Verarbeiten der Anfrage.');
        }
    };

    return (
        <div>
            <input 
                type="text" 
                value={inputValue} 
                onChange={handleInputChange} 
                placeholder="Gib hier deine Mitarbeiter-ID ein" 
            />
            <button onClick={handleScanID}>ID-Scan</button> {/* Button, der die ID prüft */}
        </div>
    );
}

export default InputField;
