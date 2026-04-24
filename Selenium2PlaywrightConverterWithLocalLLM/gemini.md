# Project Constitution (Gemini)

## Status: COMPLETE

## Data Schemas

### 1. Conversion Request (UI -> Backend/LLM)
```json
{
  "sourceCode": "String (Selenium Java)",
  "options": {
    "usePageObjectModel": true
  }
}
```

### 2. Conversion Response (Backend/LLM -> UI)
```json
{
  "files": [
    {
      "fileName": "String",
      "fileType": "page-object | test-spec",
      "content": "String"
    }
  ],
  "logs": ["String"]
}
```

## Maintenance Log
- **Phase 1 (Blueprint)**: Defined schemas and utilized Page Object Model pattern.
- **Phase 2 (Link)**: Verified Ollama local connection (`codellama`).
- **Phase 3 (Architect)**: Built Node.js backend.
- **Phase 4 (Stylize)**: Built React Frontend with Monaco Editor.
- **Phase 5 (Trigger)**: Deployed locally and documented usage.

## Architectural Invariants
1.  **The Golden Rule:** If logic changes, update `architecture/` SOPs first.
2.  **Local-First:** Dependency on local Ollama instance is critical.
3.  **Strict POM:** Output must always separate logic from tests.
