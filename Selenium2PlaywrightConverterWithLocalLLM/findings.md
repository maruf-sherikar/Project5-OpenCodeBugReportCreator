# Findings

## Research
*   **Goal**: Convert Selenium (Java/TestNG) -> Playwright (JS/TS).
*   **Pattern**: Page Object Model (POM) is mandatory.
*   **UI Requirement**: User inputs Java code -> UI displays Playwright code.

## Discoveries
*   **Input**: Raw Java code strings.
*   **Output**: Structured JS/TS code, potentially split across multiple files (Page Objects vs Tests).
*   **Integration**: Local LLM is the engine. Need to define the API contract for this.

## Constraints
*   **OS**: Windows.
*   **Tech Stack**: Vite + React (Recommended for "Premium" UI), Node.js for backend/local processing if needed, or direct browser-to-LLM if CORS allows. *Decision: Use a lightweight Node.js backend (Express) to handle file writing and LLM communication securely/reliably.*
