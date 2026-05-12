import json
import os

def generate_markdown(input_file="input.json", output_file="api_documentation.md"):
    with open(input_file, 'r') as f:
        data = json.load(f)

    md_content = f"# {data.get('api_name', 'API Documentation')}\n\n"
    md_content += f"**Base URL:** `{data.get('base_url', '')}`\n\n"
    md_content += "---\n\n"

    for endpoint in data.get('endpoints', []):
        md_content += f"## `{endpoint['method']}` {endpoint['path']}\n\n"
        
        if endpoint.get('headers'):
            md_content += "### Headers\n"
            md_content += "| Key | Value |\n|---|---|\n"
            for k, v in endpoint['headers'].items():
                md_content += f"| {k} | `{v}` |\n"
            md_content += "\n"
            
        if endpoint.get('query_params'):
            md_content += "### Query Parameters\n"
            md_content += "| Parameter | Type |\n|---|---|\n"
            for k, v in endpoint['query_params'].items():
                md_content += f"| {k} | `{v}` |\n"
            md_content += "\n"
            
        if endpoint.get('request_body'):
            md_content += "### Request Body\n"
            md_content += "```json\n"
            md_content += json.dumps(endpoint['request_body'], indent=2)
            md_content += "\n```\n\n"
            
        if endpoint.get('response'):
            md_content += "### Response\n"
            md_content += "```json\n"
            md_content += json.dumps(endpoint['response'], indent=2)
            md_content += "\n```\n\n"
            
        if endpoint.get('status_codes'):
            md_content += "### Status Codes\n"
            md_content += ", ".join([f"`{code}`" for code in endpoint['status_codes']])
            md_content += "\n\n---\n\n"

    with open(output_file, 'w') as f:
        f.write(md_content)
    
    print(f"[SUCCESS] Markdown generated at {output_file}")

if __name__ == "__main__":
    generate_markdown()
