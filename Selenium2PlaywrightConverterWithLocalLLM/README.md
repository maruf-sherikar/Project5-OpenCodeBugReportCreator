# 🚀 Selenium to Playwright Converter (Local LLM)

A professional-grade tool to intelligently convert **Selenium Java (TestNG)** test suites into **Playwright TypeScript** using the **Page Object Model (POM)** pattern. Powered by local LLM (Ollama) for maximum privacy and performance.

![UI Preview](https://github.com/MarufCode/Selenium2PlaywrightConverterWithLocalLLM/raw/master/preview.png) *(Placeholder: Add your screenshot here!)*

## ✨ Key Features

- 🏠 **Intelligent POM Support**: Automatically separates element locators and page actions from test logic.
- ⚡ **Local LLM Engine**: Uses `codellama` via [Ollama](https://ollama.ai/)—no API keys, no data leaving your machine.
- 🎨 **Modern Split-View UI**: High-fidelity code editors powered by Monaco (VS Code's engine).
- 📂 **Structured Output**: Generates separate files for Page Objects and Spec files.
- 🛡️ **TypeScript First**: Produces clean, typed, and asynchronous Playwright code.

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:

1. **Node.js**: `v18+` or `v20+` is recommended. (Verified on `v22.4.0`)
2. **Ollama**: Download and install from [ollama.ai](https://ollama.ai/).
3. **Codellama**: Run the following command to download the model:
   ```bash
   ollama pull codellama
   ```

## 🏗️ Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/MarufCode/Selenium2PlaywrightConverterWithLocalLLM.git
cd Selenium2PlaywrightConverterWithLocalLLM
```

### 2. Start the Backend API
The backend handles the communication with your local Ollama instance.
```bash
# From the root directory
node server/index.js
```
*The server will start on `http://localhost:3001`.*

### 3. Start the Frontend Dashboard
```bash
# In a new terminal
cd client
npm run dev
```
*The UI will be available at `http://localhost:5173`.*

## 📂 Project Architecture

```text
├── server/          # Express.js API (Ollama Bridge)
├── client/          # React + Vite + Monaco Editor
├── architecture/    # Technical SOPs & Protocol Docs
├── tools/           # Health checks & test scripts
└── gemini.md        # Project Constitution & Data Schemas
```

## ⚖️ License
Distributed under the MIT License.

---
*Built with ❤️ for the QA Engineering community.*
