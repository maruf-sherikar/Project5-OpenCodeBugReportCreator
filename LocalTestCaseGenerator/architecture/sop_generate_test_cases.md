# SOP: Generate Test Cases

## Goal
To generate comprehensive, structured test cases from a set of user requirements using a local LLM.

## Inputs
- **User Requirements** (String): The raw text describing the feature or user story.
- **Model Config** (Object): Settings for the LLM (default: `qwen3:4b`, temp: 0.7).

## Logic Flow
1. **Validation**: Check if `User Requirements` is not empty.
2. **Templating**:
   - Load `PROMPT_TEMPLATE` from code assets.
   - Replace `{{REQUIREMENTS}}` with `User Requirements`.
3. **Execution**:
   - Send POST request to `http://localhost:11434/api/generate`.
   - Body: `{"model": "qwen3:4b", "prompt": "...", "stream": false}`.
4. **Output**:
   - Extract `response` field from JSON.
   - Return as Markdown string.

## Edge Cases
- **Ollama Offline**: If fetch fails, return descriptive error "Ollama service unreachable".
- **Empty Response**: If model returns empty string, retry once or return error.
- **Model Missing**: If `qwen3:4b` not found, prompt user to pull it.
