# Project Constitution: Local LLM Testcase Generator with Ollama

## Data Schemas
### Input Payload
```json
{
  "user_input": "String: The feature requirements or user story",
  "model_config": {
    "model_name": "qwen3:4b", 
    "temperature": 0.7
  }
}
```

### Output Payload
```json
{
  "response": "String: Markdown formatted test cases",
  "status": "success | error"
}
```

## Behavioral Rules
- **Reliability over Speed**: Ensure test cases are accurate and functionally viable.
- **Local First**: All LLM processing via Ollama `qwen3:4b` (or configured model).
- **Template Driven**: The system MUST use the strict `prompt_template` stored in the codebase, injecting the `user_input` into it.
- **UI Interaction**: Chat-based interface where user provides input -> System acknowledges -> Stream/Show results.

## Architectural Invariants
- **Frontend**: React (Vite) + Tailwind (if requested, else CSS components) - *User Rule: "Use Vanilla CSS ... Avoid using TailwindCSS unless USER explicitly requests it"*. OK, I will use **Vanilla CSS** with a "Rich Aesthetic".
- **Backend**: Node.js (Express) to proxy requests to Ollama and inject the prompt template.
- **Integration**: Direct http call to localhost:11434 (Ollama default port).
