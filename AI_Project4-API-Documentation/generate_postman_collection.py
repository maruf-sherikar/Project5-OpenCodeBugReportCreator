import json
import uuid

def generate_postman_collection(input_file="input.json", output_file="postman_collection.json"):
    with open(input_file, 'r') as f:
        data = json.load(f)

    collection = {
        "info": {
            "_postman_id": str(uuid.uuid4()),
            "name": data.get("api_name", "API Documentation"),
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": []
    }

    base_url = data.get("base_url", "https://api.example.com")
    
    # Simple split to postman url host format
    host_parts = base_url.replace("https://", "").replace("http://", "").split("/")
    host = host_parts[0].split(".")
    base_path = host_parts[1:] if len(host_parts) > 1 else []

    for endpoint in data.get("endpoints", []):
        request_item = {
            "name": f"{endpoint['method']} {endpoint['path']}",
            "request": {
                "method": endpoint["method"],
                "header": [],
                "url": {
                    "raw": f"{base_url}{endpoint['path']}",
                    "host": host,
                    "path": base_path + [p for p in endpoint["path"].split("/") if p]
                }
            },
            "response": []
        }

        # Add headers
        if endpoint.get("headers"):
            for k, v in endpoint["headers"].items():
                request_item["request"]["header"].append({
                    "key": k,
                    "value": v,
                    "type": "text"
                })

        # Add query parameters
        if endpoint.get("query_params"):
            query_arr = []
            for k, v in endpoint["query_params"].items():
                query_arr.append({
                    "key": k,
                    "value": f"<{v}>"
                })
            request_item["request"]["url"]["query"] = query_arr
            # append query string to raw url for display simplicity
            qs = "&".join([f"{q['key']}={q['value']}" for q in query_arr])
            request_item["request"]["url"]["raw"] += f"?{qs}"

        # Add Request Body
        if endpoint.get("request_body"):
            request_item["request"]["body"] = {
                "mode": "raw",
                "raw": json.dumps(endpoint["request_body"], indent=2),
                "options": {
                    "raw": {
                        "language": "json"
                    }
                }
            }

        collection["item"].append(request_item)

    with open(output_file, 'w') as f:
        json.dump(collection, f, indent=2)

    print(f"[SUCCESS] Postman Collection JSON generated at {output_file}")

if __name__ == "__main__":
    generate_postman_collection()
