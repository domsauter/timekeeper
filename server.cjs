const express = require('express');
const fs = require('fs');
const xlsx = require('xlsx');
const path = require('path');
const cors = require('cors'); // Import the cors package

const app = express();
const port = 3001;

// Enable CORS for all origins (you can also restrict it to specific origins if needed)
app.use(cors());

// Middleware to parse JSON requests
app.use(express.json());

// Paths to the Excel file and log file
const excelFilePath = path.join(__dirname, 'src/id.xlsx');
const logFilePath = path.join(__dirname, 'src/log.txt');

// POST route to scan ID
app.post('/scan-id', (req, res) => {
    const searchID = req.body.id;

    // Read the Excel file
    const workbook = xlsx.readFile(excelFilePath);
    const worksheet = workbook.Sheets[workbook.SheetNames[0]];
    const data = xlsx.utils.sheet_to_json(worksheet);

    // Check if the ID is present
    const entry = data.find(row => row.ID.toString() === searchID);
    
    if (entry) {
        const logEntry = `${entry.ID}, ${entry.Name}, ${entry.Abteilung}, ${new Date().toLocaleString()}\n`;
        
        // Write to the log file
        fs.appendFile(logFilePath, logEntry, (err) => {
            if (err) {
                console.error('Fehler beim Schreiben in die Log-Datei:', err);
                return res.status(500).json({ success: false });
            }
            res.json({ success: true });
        });
    } else {
        res.json({ success: false });
    }
});

// Home route
app.get('/', (req, res) => {
    res.send('Willkommen bei Timekeeper! Der Server läuft.');
});

// Start the server
app.listen(port, () => {
    console.log(`Server läuft auf http://localhost:${port}`);
});
