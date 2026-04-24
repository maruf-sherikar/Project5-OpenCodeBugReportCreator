# SOP: Web Generation Flow

## 1. Request Reception
- Endpoint: `POST /generate-docs`
- Body: Raw JSON following the `INPUT SCHEMA` defined in `gemini.md`.

## 2. Processing Pipeline (Deterministic & Sequential)
Each step MUST verify the success of the previous step.

### Step 1: Validation
- Call `validate_api_input.py` on the input JSON.
- If return code != 0 or script outputs `[ERROR]`:
  - HALT execution.
  - Return HTTP 400 with the error message.

### Step 2: Normalization
- Map raw validated JSON to internal canonical format.

### Step 3: Transformation
- Execute in sequence:
  1. `generate_markdown_docs.py`
  2. `generate_openapi_json.py`
  3. `generate_postman_collection.py`

### Step 4: Storage
- Ensure all outputs are saved in the `/output` directory.

## 3. Response Generation
- Return a JSON object containing:
  - `status`: "SUCCESS"
  - `files`: List of generated filenames relative to the download endpoint.

## 4. Error Handling
- Use structured JSON responses for all failure cases.
- Logs must be persistent in the console/system logs.
