const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const { PROMPT_TEMPLATE } = require('./prompt_template');

const app = express();
const PORT = 3000;

const path = require('path');

app.use(cors());
app.use(bodyParser.json());

// Serve Static Frontend (Build first)
app.use(express.static(path.join(__dirname, '../client/dist')));

// Real endpoint implementation
app.post('/api/generate', async (req, res) => {
    const { user_input, model_config } = req.body;
    console.log("Received input:", user_input);

    if (!user_input) {
        return res.status(400).json({ status: 'error', message: 'User input is required' });
    }

    try {
        // 1. Prepare Prompt
        const finalPrompt = PROMPT_TEMPLATE.replace('{{REQUIREMENTS}}', user_input);
        console.log("📝 Generating with prompt length:", finalPrompt.length);

        // 2. Call Ollama (Stream: true)
        const model = model_config?.model_name || "qwen3:4b";
        // Force IPv4 loopback to avoid Node.js localhost resolution issues
        const response = await fetch("http://127.0.0.1:11434/api/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                model: model,
                prompt: finalPrompt,
                stream: true
            })
        });

        if (!response.ok) {
            throw new Error(`Ollama API Error: ${response.statusText}`);
        }

        // 3. Pipe Response Stream to Client
        res.setHeader('Content-Type', 'text/plain; charset=utf-8');

        // Node 18+ fetch body is an async iterable
        const decoder = new TextDecoder();
        let buffer = '';

        for await (const chunk of response.body) {
            const text = decoder.decode(chunk, { stream: true });
            buffer += text;

            let lines = buffer.split('\n');
            buffer = lines.pop(); // Keep the last incomplete line in buffer

            for (const line of lines) {
                if (!line.trim()) continue;
                try {
                    const json = JSON.parse(line);
                    if (json.response) {
                        res.write(json.response);
                    }
                } catch (e) {
                    console.error("Error parsing JSON chunk", e);
                }
            }
        }
        res.end();
        console.log("✅ Generation complete (Streamed).");

    } catch (error) {
        console.error("❌ Generation Failed:", error);

        // Prevent double-response crash
        if (!res.headersSent) {
            res.status(500).json({
                status: 'error',
                message: 'Failed to generate test cases',
                error: error.message
            });
        } else {
            // If headers were already sent, we can't send JSON. 
            // End the stream with an error indicator if possible, or just end it.
            res.write("\n\n[Error: Connection to model failed]");
            res.end();
        }
    }
});

app.listen(PORT, '127.0.0.1', () => {
    console.log(`Server running on http://127.0.0.1:${PORT}`);
});
