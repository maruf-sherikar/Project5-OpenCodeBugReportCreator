import json
import sys

def validate_input(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] File '{file_path}' not found.")
        return False
    except json.JSONDecodeError:
        print(f"[ERROR] File '{file_path}' contains invalid JSON.")
        return False

    required_top_level = ['api_name', 'base_url', 'endpoints']
    for req in required_top_level:
        if req not in data:
            print(f"[ERROR] Missing required top-level field: '{req}'")
            return False

    if not isinstance(data.get('endpoints'), list):
        print("[ERROR] 'endpoints' must be a list.")
        return False

    required_endpoint_fields = ['path', 'method', 'headers', 'query_params', 'request_body', 'response', 'status_codes']
    allowed_methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']

    for i, endpoint in enumerate(data['endpoints']):
        for req in required_endpoint_fields:
            if req not in endpoint:
                print(f"[ERROR] Endpoint at index {i} missing required field: '{req}'")
                return False
        
        if endpoint.get('method') not in allowed_methods:
            print(f"[ERROR] Endpoint at index {i} has invalid method: '{endpoint.get('method')}'. Allowed: {allowed_methods}")
            return False

    print("[SUCCESS] API Input Validation Passed. JSON strictly matches the INPUT SCHEMA.")
    return True

if __name__ == "__main__":
    target_file = 'input.json'
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
    
    validate_input(target_file)
