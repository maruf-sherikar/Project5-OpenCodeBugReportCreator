
// Native fetch in Node 18+

async function debugStream() {
    const model = "qwen3:4b";
    const prompt = "Create the testcase for app.vwo.com";

    console.log("🚀 Debugging Ollama Stream...");
    console.log(`Target: http://127.0.0.1:11434/api/generate`);

    try {
        const response = await fetch("http://127.0.0.1:11434/api/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                model: model,
                prompt: prompt,
                stream: true
            })
        });

        console.log(`✅ Response Status: ${response.status}`);

        if (!response.ok) {
            console.error("Response not OK");
            return;
        }

        // Node 18 native fetch or node-fetch
        if (response.body.getReader) {
            // Browser-like
            console.log("Using getReader()");
        } else {
            // Node stream
            console.log("Using Node Stream");
            for await (const chunk of response.body) {
                console.log("📦 Received chunk length:", chunk.length);
                console.log("Chunk preview:", chunk.toString().slice(0, 50));
                break; // Just one to prove it works
            }
        }
        console.log("✅ Stream verified.");

    } catch (error) {
        console.error("❌ Stream failed:", error);
    }
}

debugStream();
