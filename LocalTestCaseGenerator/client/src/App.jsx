import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import './index.css';

function App() {
  const [input, setInput] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleGenerate = async () => {
    if (!input.trim()) return;

    setLoading(true);
    setError('');
    setResponse(''); // Clear previous

    try {
      const res = await fetch('http://127.0.0.1:3000/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_input: input,
          model_config: { model_name: 'qwen3:4b' }
        }),
      });

      if (!res.ok) {
        throw new Error(`Server error: ${res.statusText}`);
      }

      // Read the stream
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let done = false;

      while (!done) {
        const { value, done: doneReading } = await reader.read();
        done = doneReading;
        const chunkValue = decoder.decode(value, { stream: true });
        setResponse((prev) => prev + chunkValue);
      }

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>🚀 Test Case Generator</h1>

      <div className="input-section glass">
        <h3>User Requirements</h3>
        <textarea
          placeholder="Paste your feature requirements or user story here... (e.g. As a user, I want to login with email and password...)"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={loading}
        />
        <button onClick={handleGenerate} disabled={loading || !input.trim()}>
          {loading ? <><div className="spinner"></div> Generating...</> : 'Generate Test Cases'}
        </button>
        {error && <p style={{ color: '#ef4444', marginTop: '0.5rem' }}>⚠️ {error}</p>}
      </div>

      {(response || loading) && (
        <div className="output-section glass">
          <h3>Generated Test Cases</h3>
          {loading && !response && <p style={{ color: 'var(--text-secondary)' }}>Thinking (this may take a moment)...</p>}
          <div className="markdown-content">
            <ReactMarkdown>{response}</ReactMarkdown>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
