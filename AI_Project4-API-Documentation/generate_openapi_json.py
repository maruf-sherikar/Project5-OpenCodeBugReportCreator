import json

def generate_openapi(input_file="input.json", output_file="openapi_spec.json"):
    with open(input_file, 'r') as f:
        data = json.load(f)

    openapi = {
        "openapi": "3.0.0",
        "info": {
            "title": data.get("api_name", "API Documentation"),
            "version": "1.0.0"
        },
        "servers": [
            {
                "url": data.get("base_url", "https://api.example.com")
            }
        ],
        "paths": {}
    }

    for endpoint in data.get("endpoints", []):
        path = endpoint["path"]
        method = endpoint["method"].lower()

        if path not in openapi["paths"]:
            openapi["paths"][path] = {}

        operation = {
            "responses": {}
        }
        
        # Add parameters (headers and query params)
        parameters = []
        if endpoint.get("headers"):
            for k, v in endpoint["headers"].items():
                parameters.append({
                    "name": k,
                    "in": "header",
                    "schema": {"type": "string", "example": v}
                })
                
        if endpoint.get("query_params"):
            for k, v in endpoint["query_params"].items():
                parameters.append({
                    "name": k,
                    "in": "query",
                    "schema": {"type": v}
                })
        
        if parameters:
            operation["parameters"] = parameters

        # Add request body
        if endpoint.get("request_body"):
            operation["requestBody"] = {
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "example": endpoint["request_body"]
                        }
                    }
                }
            }

        # Add responses
        for code in endpoint.get("status_codes", [200]):
            operation["responses"][str(code)] = {
                "description": f"{code} Response",
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "example": endpoint.get("response", {})
                        }
                    }
                }
            }

        openapi["paths"][path][method] = operation

    with open(output_file, 'w') as f:
        json.dump(openapi, f, indent=2)

    print(f"[SUCCESS] OpenAPI JSON generated at {output_file}")

if __name__ == "__main__":
    generate_openapi()
