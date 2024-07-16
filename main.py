import json
import requests
import argparse
from urllib.parse import urlparse, urlunparse

# Load Postman collection
def load_postman_collection(collection_path):
    with open(collection_path, 'r') as file:
        collection = json.load(file)
    return collection

# Load Postman environment file
def load_postman_environment(environment_path):
    if environment_path:
        with open(environment_path, 'r') as file:
            environment = json.load(file)
    else:
        environment = {}
    return environment

# Resolve variables from both collection and environment
def resolve_variables(collection, environment):
    variables = {}

    # Collect variables from environment
    if 'values' in environment:
        for value in environment['values']:
            variables[value['key']] = value['value']

    # Collect variables from collection
    if 'variable' in collection:
        for variable in collection['variable']:
            variables[variable['key']] = variable['value']

    return variables

# Resolve variables in a URL
def resolve_url_variables(url, variables):
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme if parsed_url.scheme else 'https'
    netloc = parsed_url.netloc if parsed_url.netloc else variables.get('baseUrl', '')
    path = parsed_url.path
    query = parsed_url.query

    # Resolve variables in netloc, path, and query
    netloc = netloc.format(**variables)
    path = path.format(**variables)
    query = query.format(**variables)

    # Reconstruct the URL with resolved variables
    resolved_url = urlunparse((scheme, netloc, path, '', query, ''))
    return resolved_url

# Send HTTP request using a default proxy
def send_request(request, variables):
    method = request['method']
    url = resolve_url_variables(request['url']['raw'], variables)
    headers = {header['key']: header['value'] for header in request.get('header', [])}
    data = None

    if 'body' in request:
        mode = request['body']['mode']
        if mode == 'raw':
            data = request['body']['raw'].format(**variables)
        elif mode == 'urlencoded':
            data = {item['key']: item['value'].format(**variables) for item in request['body']['urlencoded']}
        elif mode == 'formdata':
            data = {item['key']: item['value'].format(**variables) for item in request['body']['formdata']}

    proxy = 'http://127.0.0.1:8080'  # Define your default proxy URL here

    proxies = {
        "http": proxy,
        "https": proxy
    }

    try:
        requests.request(method, url, headers=headers, data=data, proxies=proxies)
    except requests.exceptions.MissingSchema as e:
        print(f"Error sending request: {e}")

# Main function
def main():
    parser = argparse.ArgumentParser(description='Send Postman collection requests.')
    parser.add_argument('collection', type=str, help='Path to the Postman collection JSON file')
    parser.add_argument('--environment', type=str, help='Path to the Postman environment JSON file (optional)')
    args = parser.parse_args()

    collection = load_postman_collection(args.collection)
    environment = load_postman_environment(args.environment)
    variables = resolve_variables(collection, environment)

    for item in collection['item']:
        if 'request' in item:
            request = item[a'request']
            send_request(request, variables)

if __name__ == "__main__":
    main()
