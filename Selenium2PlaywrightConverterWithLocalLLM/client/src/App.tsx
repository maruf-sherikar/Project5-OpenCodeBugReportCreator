import { useState } from 'react';
import Editor from '@monaco-editor/react';
import { Play, FileCode, Terminal } from 'lucide-react';
import { convertCode, type ConversionResponse } from './api';
import './index.css';

function App() {
  const [sourceCode, setSourceCode] = useState<string>(
    `package com.example.tests;

import org.testng.annotations.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public class LoginTest {
    @Test
    public void testLogin() {
        WebDriver driver = new ChromeDriver();
        driver.get("https://example.com/login");
        driver.findElement(By.id("username")).sendKeys("admin");
        driver.findElement(By.id("password")).sendKeys("secret");
        driver.findElement(By.id("submit")).click();
        
        String title = driver.getTitle();
        assert title.equals("Dashboard");
        
        driver.quit();
    }
}`
  );

  const [conversionResult, setConversionResult] = useState<ConversionResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeFileIndex, setActiveFileIndex] = useState(0);

  const handleConvert = async () => {
    setLoading(true);
    setConversionResult(null);
    try {
      const result = await convertCode(sourceCode, true);
      setConversionResult(result);
      if (result.files && result.files.length > 0) {
        setActiveFileIndex(0);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const activeFile = conversionResult?.files?.[activeFileIndex];

  return (
    <div className="h-full flex flex-col bg-dark text-white" style={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <header className="flex items-center justify-between p-4 border-b bg-darker" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '1rem', borderBottom: '1px solid #30363d', background: '#010409' }}>
        <div className="flex items-center gap-2" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Terminal size={24} className="text-green-500" style={{ color: '#238636' }} />
          <h1 className="font-bold text-lg" style={{ fontWeight: 'bold', fontSize: '1.125rem', margin: 0 }}>Selenium &rarr; Playwright Converter</h1>
        </div>
        <div>
          <button
            onClick={handleConvert}
            disabled={loading}
            className="primary"
            style={{
              background: '#238636',
              color: 'white',
              padding: '0.5rem 1rem',
              borderRadius: '6px',
              border: 'none',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem'
            }}
          >
            {loading ? 'Converting...' : <><Play size={16} /> Convert to Playwright</>}
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex overflow-hidden" style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>

        {/* Left: Input (Java) */}
        <section className="flex-1 flex flex-col border-r" style={{ flex: 1, display: 'flex', flexDirection: 'column', borderRight: '1px solid #30363d' }}>
          <div style={{ padding: '0.5rem', background: '#010409', fontSize: '0.875rem', fontWeight: 'bold', borderBottom: '1px solid #30363d' }}>
            Input: Selenium Java
          </div>
          <div style={{ flex: 1 }}>
            <Editor
              height="100%"
              defaultLanguage="java"
              theme="vs-dark"
              value={sourceCode}
              onChange={(val) => setSourceCode(val || "")}
              options={{ minimap: { enabled: false }, fontSize: 14 }}
            />
          </div>
        </section>

        {/* Right: Output (Typescript) */}
        <section className="flex-1 flex flex-col" style={{ flex: 1, display: 'flex', flexDirection: 'column', background: '#0d1117' }}>
          {/* Output Tabs */}
          <div style={{ display: 'flex', background: '#010409', borderBottom: '1px solid #30363d', overflowX: 'auto' }}>
            {!conversionResult && !loading && (
              <div style={{ padding: '0.5rem', fontSize: '0.875rem', color: '#8b949e', fontStyle: 'italic' }}>No output yet. Click Convert.</div>
            )}

            {loading && (
              <div style={{ padding: '0.5rem', fontSize: '0.875rem', color: '#d29922' }}>
                ⏳ Generating... Please wait (Local LLM)
              </div>
            )}

            {conversionResult?.error && (
              <div style={{ padding: '0.5rem', fontSize: '0.875rem', color: '#f85149' }}>
                Error: {conversionResult.error}
              </div>
            )}

            {conversionResult?.files?.map((file, idx) => (
              <button
                key={idx}
                onClick={() => setActiveFileIndex(idx)}
                style={{
                  padding: '0.5rem 1rem',
                  fontSize: '0.875rem',
                  background: idx === activeFileIndex ? '#161b22' : 'transparent',
                  color: idx === activeFileIndex ? 'white' : '#8b949e',
                  border: 'none',
                  borderBottom: idx === activeFileIndex ? '2px solid #238636' : 'none',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.4rem'
                }}
              >
                <FileCode size={14} />
                {file.fileName}
              </button>
            ))}
          </div>

          {/* Output Editor */}
          <div style={{ flex: 1, position: 'relative' }}>
            {activeFile ? (
              <Editor
                height="100%"
                language="typescript"
                theme="vs-dark"
                value={activeFile.content}
                options={{ readOnly: true, minimap: { enabled: false }, fontSize: 14 }}
              />
            ) : (
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: '#484f58' }}>
                Result will appear here
              </div>
            )}
          </div>
        </section>

      </main>
    </div>
  );
}

export default App;
