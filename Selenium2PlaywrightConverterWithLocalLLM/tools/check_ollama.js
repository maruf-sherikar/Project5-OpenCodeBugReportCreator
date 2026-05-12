const http = require('http');

const checkOllama = async () => {
    const modelName = 'codellama';
    const options = {
        hostname: 'localhost',
        port: 11434,
        path: '/api/tags',
        method: 'GET',
    };

    console.log(`Checking connection to http://${options.hostname}:${options.port}...`);

    const req = http.request(options, (res) => {
        let data = '';

        res.on('data', (chunk) => {
            data += chunk;
        });

        res.on('end', () => {
            if (res.statusCode === 200) {
                console.log('✅ Ollama is reachable.');
                try {
                    const models = JSON.parse(data).models || [];
                    const found = models.some((m) => m.name.startsWith(modelName));

                    if (found) {
                        console.log(`✅ Model '${modelName}' found.`);
                        performHandshake();
                    } else {
                        console.log(`⚠️ Model '${modelName}' NOT found in local library.`);
                        console.log(`Please run: ollama pull ${modelName}`);
                        process.exit(1);
                    }
                } catch (e) {
                    console.error('❌ Error parsing response:', e.message);
                    process.exit(1);
                }
            } else {
                console.log(`❌ Ollama returned status: ${res.statusCode}`);
                process.exit(1);
            }
        });
    });

    req.on('error', (e) => {
        console.error(`❌ Ollama is NOT reachable: ${e.message}`);
        process.exit(1);
    });

    req.end();
};

const performHandshake = () => {
    console.log('Attempting handshake (simple generation)...');
    const postData = JSON.stringify({
        model: 'codellama',
        prompt: 'Write a hello world in javascript',
        stream: false,
    });

    const options = {
        hostname: 'localhost',
        port: 11434,
        path: '/api/generate',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': postData.length,
        },
    };

    const req = http.request(options, (res) => {
        let data = '';

        res.on('data', (chunk) => {
            data += chunk;
        });

        res.on('end', () => {
            if (res.statusCode === 200) {
                console.log('✅ Handshake successful! Response received.');
                try {
                    const json = JSON.parse(data);
                    console.log(`Sample: ${json.response.substring(0, 50)}...`);
                } catch (e) {
                    console.log('Raw response received (parsing failed but connection works).');
                }
            } else {
                console.log(`❌ Handshake failed: ${res.statusCode}`);
                process.exit(1);
            }
        });
    });

    req.on('error', (e) => {
        console.error(`❌ Handshake error: ${e.message}`);
        process.exit(1);
    });

    req.write(postData);
    req.end();
};

checkOllama();
