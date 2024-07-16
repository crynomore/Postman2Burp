import json
import requests

# Load Postman collection
def load_postman_collection(collection_path):
    with open(collection_path, 'r') as file:
        collection = json.load(file)
    return collection

# Resolve variables in the Postman collection
def resolve_variables(collection, variables):
    def resolve(value):
        for var in variables:
            value = value.replace(f"{{{{{var['key']}}}}}", var['value'])
        return value
    
    for item in collection['item']:
        if 'request' in item:
            request = item['request']
            request['url']['raw'] = resolve(request['url']['raw'])
            if 'body' in request:
                request['body']['raw'] = resolve(request['body']['raw'])

# Send cURL request using a proxy
def send_request(request, proxy):
    method = request['method']
    url = request['url']['raw']
    headers = {header['key']: header['value'] for header in request.get('header', [])}
    data = request.get('body', {}).get('raw', '')

    proxies = {
        "http": proxy,
        "https": proxy
    }

    response = requests.request(method, url, headers=headers, data=data, proxies=proxies)
    return response

# Main function
def main():
    collection_path = 'path_to_your_postman_collection.json'
    proxy = 'http://127.0.0.1:8080'

    collection = load_postman_collection(collection_path)
    variables = collection.get('variable', [])
    resolve_variables(collection, variables)

    for item in collection['item']:
        if 'request' in item:
            request = item['request']
            response = send_request(request, proxy)
            print(f"Response from {request['url']['raw']}: {response.status_code}")
            print(response.text)

if __name__ == "__main__":
    main()
