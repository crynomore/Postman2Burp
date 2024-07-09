import json
import requests

# Load Postman collection
def load_postman_collection(file_path):
    with open(file_path, 'r') as file:
        collection = json.load(file)
    return collection

# Load Postman environment
def load_postman_environment(file_path):
    with open(file_path, 'r') as file:
        environment = json.load(file)
    return environment

# Resolve variables in request URL and body
def resolve_variables(data, environment):
    variables = {item['key']: item['value'] for item in environment['values']}
    if isinstance(data, str):
        for key, value in variables.items():
            data = data.replace(f"{{{{{key}}}}}", value)
    elif isinstance(data, dict):
        for key, value in data.items():
            data[key] = resolve_variables(value, environment)
    return data

# Send request to Burp Suite Repeater
def send_to_burp_repeater(request_data, burp_host, burp_port):
    headers = {"Content-Type": "application/json"}
    proxy = {
        'http': f'http://{burp_host}:{burp_port}',
        'https': f'http://{burp_host}:{burp_port}'
    }
    response = requests.post(
        f'http://{burp_host}:{burp_port}/burp/repeater', 
        data=json.dumps(request_data), 
        headers=headers, 
        proxies=proxy
    )
    return response

# Main function
def main(collection_file, environment_file, burp_host, burp_port):
    # Load Postman collection and environment
    collection = load_postman_collection(collection_file)
    environment = load_postman_environment(environment_file)

    for item in collection['item']:
        request = item['request']
        url = request['url']['raw']
        url = resolve_variables(url, environment)
        
        body = None
        if request.get('body') and request['body'].get('raw'):
            body = resolve_variables(request['body']['raw'], environment)
        
        headers = {header['key']: resolve_variables(header['value'], environment) for header in request['header']}
        
        # Prepare request data for Burp Repeater
        request_data = {
            "method": request['method'],
            "url": url,
            "headers": headers,
            "body": body
        }

        # Send request to Burp Repeater
        response = send_to_burp_repeater(request_data, burp_host, burp_port)
        print(f"Sent {request['method']} request to {url}, response: {response.status_code}")

# Example usage
if __name__ == "__main__":
    collection_file = 'path_to_postman_collection.json'
    environment_file = 'path_to_postman_environment.json'
    burp_host = 'localhost'
    burp_port = 8080

    main(collection_file, environment_file, burp_host, burp_port)
