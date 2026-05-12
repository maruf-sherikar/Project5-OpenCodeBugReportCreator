
async function testOllama() {
    const model = "qwen3:4b";
    const prompt = "Say 'Handshake Protocol Initiated' if you can hear me.";

    console.log(`📡 Sending handshake to Ollama [${model}]...`);

    try {
        const response = await fetch("http://localhost:11434/api/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                model: model,
                prompt: prompt,
                stream: false
            }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log("✅ Connection Successful!");
        console.log("📝 Model Response:", data.response);
    } catch (error) {
        console.error("❌ Connection Failed:", error);
        process.exit(1);
    }
}

testOllama();
