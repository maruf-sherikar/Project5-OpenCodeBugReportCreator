from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import json
import subprocess
import uuid

app = FastAPI(title="API Documentation Generator")

# Allow all CORS for simple connectivity
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.get("/")
def serve_frontend():
    """Serve the minimal web frontend."""
    return FileResponse("index.html")

def run_tool(script_name, args=[]):
    """Wrapper to call deterministic tools via subprocess."""
    print(f"[PROCESS] Executing: python {script_name} {' '.join(args)}")
    result = subprocess.run(["python", script_name] + args, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] {script_name} failed: {result.stderr}")
        return False, result.stderr or result.stdout
    print(f"[SUCCESS] {script_name} completed.")
    return True, result.stdout

@app.get("/health")
def health_check():
    """Verify backend is reachable."""
    return {"status": "SUCCESS", "message": "Backend is reachable."}

@app.get("/test-write")
def test_write():
    """Verify file system write/read permissions for /output."""
    try:
        test_file = os.path.join(OUTPUT_DIR, "handshake_test.txt")
        with open(test_file, 'w') as f:
            f.write("System Pilot handshake successful.")
        return {"status": "SUCCESS", "message": f"Successfully wrote to {OUTPUT_DIR}/.", "test_file": test_file}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

@app.post("/generate-docs")
async def generate_docs(payload: dict = Body(...)):
    """
    Primary orchestration endpoint.
    Follows Phase 3 Architect logic: Validate -> Normalize -> Generate.
    """
    request_id = str(uuid.uuid4())[:8]
    temp_input = f"temp_input_{request_id}.json"
    
    try:
        # 0. Save raw input
        with open(temp_input, 'w') as f:
            json.dump(payload, f)
            
        # 1. Validate
        success, output = run_tool("validate_api_input.py", [temp_input])
        if not success:
            raise HTTPException(status_code=400, detail=f"Validation Failed: {output}")
            
        # 2. Normalize
        success, output = run_tool("normalize_api_data.py", [temp_input])
        if not success:
            raise HTTPException(status_code=500, detail="Normalization Layer Error")
            
        # 3. Transform
        scripts = ["generate_markdown_docs.py", "generate_openapi_json.py", "generate_postman_collection.py"]
        for script in scripts:
            success, output = run_tool(script)
            if not success:
                raise HTTPException(status_code=500, detail=f"Generation Layer Error: {script}")
        
        # 4. Final Verification
        files = ["api_documentation.md", "openapi_spec.json", "postman_collection.json"]
        # Move to output dir (simple implementation for single user)
        for f_name in files:
            if os.path.exists(f_name):
                os.replace(f_name, os.path.join(OUTPUT_DIR, f_name))
        
        return {
            "status": "SUCCESS",
            "request_id": request_id,
            "files": files
        }
        
    finally:
        if os.path.exists(temp_input):
            os.remove(temp_input)

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Serve generated files from the output directory."""
    file_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")
    return FileResponse(path=file_path, filename=filename)
