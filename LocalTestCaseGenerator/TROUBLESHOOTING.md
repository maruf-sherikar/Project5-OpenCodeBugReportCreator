
# Troubleshooting: Ollama Stalled

It appears that your local **Ollama** instance is responsive to basic health checks (`/api/version` works), but is **hanging indefinitely** when trying to generate text with the model `qwen3:4b`.

## Observed Behavior
- **Backend Logs**: We see your request arriving (`Received input: ...`).
- **Ollama Status**: The call to `http://127.0.0.1:11434/api/generate` never returns a response.
- **Test**: Even a simple "hi" prompt via terminal takes > 30s with no response.

## Recommended Fix
1. **Restart Ollama**:
   - Close the Ollama app from your system tray.
   - Or run `taskkill /IM ollama_app.exe /F` (if applicable) in your terminal.
   - Start Ollama again.
2. **Check Model**:
   - Run `ollama run qwen3:4b "test"` in your separate terminal to see if it works interactively.
   - If it fails, try pulling it again: `ollama pull qwen3:4b`.

Once Ollama is unstuck, the Web UI should work immediately without code changes.
