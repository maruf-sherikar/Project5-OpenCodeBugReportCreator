const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const { convertCode } = require('./converter'); // We'll implement this next

const app = express();
const PORT = 3001; // Avoid 3000 common port

app.use(cors());
app.use(bodyParser.json({ limit: '10mb' })); // Allow large code payloads

// Health Check
app.get('/api/health', (req, res) => {
    res.json({ status: 'ok', message: 'Backend is running' });
});

// Conversion Endpoint
app.post('/api/convert', async (req, res) => {
    try {
        const { sourceCode, options } = req.body;
        if (!sourceCode) {
            return res.status(400).json({ error: 'Source code is required' });
        }

        console.log(`Received conversion request for code of length ${sourceCode.length}`);

        const result = await convertCode(sourceCode, options);
        res.json(result);
    } catch (error) {
        console.error('Conversion Failed:', error.message);
        res.status(500).json({ error: error.message });
    }
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
