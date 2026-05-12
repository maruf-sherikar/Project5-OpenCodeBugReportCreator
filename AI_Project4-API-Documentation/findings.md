# findings.md — Constraints & Observations

## 1. Supported API Formats
- [x] **RESTful APIs**
  - Expected structures: Resource-based URLs, standard HTTP methods.

## 2. Configuration & Discovery Results
- **North Star:** Developer-friendly API documentation in Markdown format (Primary/Mandatory). Optional generation of OpenAPI (Swagger JSON) and Postman Collection (v2.1).
- **Integrations:** Postman (Collections, API key supported), Swagger/OpenAPI (JSON export), GitHub (Optional, token supported).
- **Source of Truth:** Primary is Raw JSON (strict schema-based). Secondary is Postman Collection. Manual text parsed ONLY if it conforms to schema.
- **Delivery Payload:** Primary is Single Markdown (`.md`) file. Secondary outputs are OpenAPI JSON file and Postman Collection JSON. All structured and consistent.

## 3. Required Fields for Documentation Generation
To successfully generate a document, the input *must* contain or imply:
1. **Endpoint URL/Path**: e.g., `/api/v1/users`
2. **HTTP Method**: e.g., `GET`, `POST`, `PUT`, `DELETE`, `PATCH`
3. **Headers**: Explicitly defined authentication or content-type headers. (e.g., `Authorization: Bearer <token>`)
4. **Request Body Schema**: Required for POST/PUT/PATCH. Must describe fields, types, and constraints.
5. **Response Schema**: Expected output format (usually JSON) with status codes (e.g., 200 OK, 400 Bad Request).

*Note: If any of these are missing from the raw input, the system must trigger clarification.*

## 3. Documentation Standards
- **Standard**: Swagger / OpenAPI 3.0 inspired structure.
- **Format**: Markdown (`.md`) primarily, configurable to JSON/YAML for Swagger UI import.
- **Aesthetic**: Clean, structured tables for parameters, clear code blocks for payloads, explicit status code definitions.
