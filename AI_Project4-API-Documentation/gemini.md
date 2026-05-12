# gemini.md — Project Constitution

## 1. Input API Schema (Expected Raw Format)
The agent expects input that strictly maps to the following conceptual schema:
```json
{
  "api_name": "string",
  "base_url": "string",
  "endpoints": [
    {
      "path": "string",
      "method": "GET|POST|PUT|DELETE",
      "headers": {},
      "query_params": {},
      "request_body": {},
      "response": {},
      "status_codes": []
    }
  ]
}
```

## 2. Output Documentation Schema
The documentation output will be generated to match the following structured format:
```json
{
  "title": "string",
  "description": "string",
  "endpoints": [
    {
      "name": "string",
      "method": "string",
      "url": "string",
      "headers": [],
      "params": [],
      "request_example": {},
      "response_example": {},
      "status_codes": []
    }
  ]
}
```

## 3. Rules for Missing/Invalid Input
- **Rule 1 (No Assumptions)**: If `endpoint`, `method`, or a critical `request_body` is missing, DO NOT hallucinate them.
- **Rule 2 (Clarification)**: Respond to the user with a specific question: *"The [Field Name] is missing for the provided API context. Please provide it before documentation can be generated."*
- **Rule 3 (Type Enforcement)**: If the input implies an invalid type, flag it immediately.

## 4. Behavioral Rules
- **No Hallucination**: Never guess or invent missing fields, headers, request bodies, or responses.
- **Strict Validation**: Always ask for missing request/response definitions.
- **Formatting Consistency**: Maintain consistent layout, structure, and design across all generated API documentation.
- **Tone**: Always use a professional, direct developer tone in warnings, clarifications, and the final documentation.
