# Server Architecture (Back-End)

## Tech Stack
- **Runtime**: Node.js
- **Framework**: Express.js (Lightweight API server)
- **CORS**: Enabled for local development (UI on port 5173, Server on 3000)

## Endpoints

### `POST /api/convert`
- **Purpose**: Converts Java Selenium code to Playwright TS.
- **Input**: `{ sourceCode: string, options: object }` (Defined in `gemini.md`)
- **Process**:
    1.  Receives source code.
    2.  Constructs a prompt for Ollama/Codellama.
    3.  Calls Ollama API (`POST /api/generate`).
    4.  Parses the response.
    5.  Returns the structured code.
- **Output**: `{ files: array, logs: array }`

### `GET /api/health`
- **Purpose**: Check server and Ollama connectivity.

## File Structure
- `server/index.js` (Entry point)
- `server/ollama.js` (Ollama client wrapper)
- `server/parser.js` (Response parsing logic)
