const http = require('http');

const OLLAMA_HOST = 'localhost';
const OLLAMA_PORT = 11434;
const MODEL = 'codellama';

const SYSTEM_PROMPT = `
You are an expert Test Automation Engineer.
Your task is to convert Selenium Java (TestNG) code into Playwright TypeScript.

**RULES**:
1. Use the **Page Object Model (POM)** pattern.
2. Use modern TypeScript syntax (async/await, strict types).
3. Use Playwright best practices (e.g., use 'waiting' locators, avoid 'page.$').
4. **IMPORTANT**: Return the response strictly as a JSON object with the following structure. Do NOT wrap it in markdown code blocks. Just valid JSON.

json_response_format:
{
  "files": [
    {
      "fileName": "TheSuggestedFileName.ts",
      "fileType": "page-object", // or "test-spec"
      "content": "Full Source Code Here" 
    }
  ],
  "logs": ["Explanation of what changed"]
}
`;

async function callOllama(prompt) {
    return new Promise((resolve, reject) => {
        const postData = JSON.stringify({
            model: MODEL,
            prompt: prompt,
            system: SYSTEM_PROMPT, // Ollama supports system prompts
            stream: false,
            format: "json", // Force JSON mode
            options: {
                temperature: 0.1 // Low temperature for deterministic code
            }
        });

        const options = {
            hostname: OLLAMA_HOST,
            port: OLLAMA_PORT,
            path: '/api/generate',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(postData),
            },
        };

        const req = http.request(options, (res) => {
            let data = '';
            res.on('data', (chunk) => data += chunk);
            res.on('end', () => {
                if (res.statusCode === 200) {
                    try {
                        const json = JSON.parse(data);
                        resolve(json.response);
                    } catch (e) {
                        reject(new Error(`Failed to parse Ollama response: ${e.message}`));
                    }
                } else {
                    reject(new Error(`Ollama API Error: ${res.statusCode}`));
                }
            });
        });

        req.on('error', (e) => reject(e));
        req.write(postData);
        req.end();
    });
}

function parseResponse(rawResponse) {
    // Attempt to extract JSON if it was wrapped in markdown despite instructions
    let jsonStr = rawResponse.trim();
    if (jsonStr.startsWith('```json')) {
        jsonStr = jsonStr.replace(/^```json/, '').replace(/```$/, '');
    } else if (jsonStr.startsWith('```')) {
        jsonStr = jsonStr.replace(/^```/, '').replace(/```$/, '');
    }

    try {
        return JSON.parse(jsonStr);
    } catch (e) {
        console.error("Failed to parse JSON from LLM:", rawResponse);
        throw new Error("LLM returned invalid JSON format.");
    }
}

async function convertCode(sourceCode, options) {
    const userPrompt = `
    Here is the Selenium Java code to convert:
    
    ${sourceCode}
    
    Convert this to Playwright TypeScript using Page Object Model.
    `;

    console.log("Sending prompt to Ollama...");
    const llmResponse = await callOllama(userPrompt);
    console.log(`Received response from Ollama (Length: ${llmResponse.length}).`);

    return parseResponse(llmResponse);
}

module.exports = { convertCode };
