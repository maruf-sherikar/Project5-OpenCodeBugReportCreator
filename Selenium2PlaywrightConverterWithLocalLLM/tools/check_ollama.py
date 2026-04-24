import requests
import json
import sys

def check_ollama(model_name="codellama"):
    base_url = "http://localhost:11434"
    
    # 1. Check if Ollama is running
    try:
        print(f"Checking connection to {base_url}...")
        requests.get(base_url)
        print("✅ Ollama is reachable.")
    except requests.exceptions.ConnectionError:
        print("❌ Ollama is NOT running or not reachable on port 11434.")
        return False

    # 2. Check if model exists
    print(f"Checking for model: {model_name}...")
    try:
        resp = requests.get(f"{base_url}/api/tags")
        models = resp.json().get('models', [])
        found = any(m['name'].startswith(model_name) for m in models)
        
        if found:
            print(f"✅ Model '{model_name}' found.")
        else:
            print(f"⚠️ Model '{model_name}' NOT found in local library.")
            print("Running 'ollama pull codellama' might be needed.")
            # We won't auto-pull as it might be large, just warn.
            
    except Exception as e:
        print(f"❌ Error listing models: {e}")
        return False

    # 3. Handshake (Simple Generation)
    print("Attempting handshake (simple generation)...")
    payload = {
        "model": model_name,
        "prompt": "Write a hello world in python",
        "stream": False
    }
    
    try:
        res = requests.post(f"{base_url}/api/generate", json=payload)
        if res.status_code == 200:
            print("✅ Handshake successful! Response received.")
            print(f"Sample: {res.json().get('response', '')[:50]}...")
            return True
        else:
            print(f"❌ Handshake failed: {res.status_code} - {res.text}")
            return False
    except Exception as e:
        print(f"❌ Handshake error: {e}")
        return False

if __name__ == "__main__":
    success = check_ollama()
    if not success:
        sys.exit(1)
