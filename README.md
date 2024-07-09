# Postman2Burp
This script allows you to import Postman API collections into Burp Suite, send the requests to the Repeater, and handle variable resolution.

# Features
- Load Postman Collection: Reads a Postman collection JSON file.
- Load Postman Environment: Reads a Postman environment JSON file.
- Resolve Variables: Replaces variables in the request URL, headers, and body with actual values from the environment.
- Send Requests to Burp Suite Repeater: Uses Burp Suite's API to send the resolved requests to the Repeater.

# Requirements
- Python 3
- requests library

# Installation
- Clone the repository
- `pip install requests`

# Usage
Prepare your Postman collection and environment JSON files.

- collection_file: Path to your Postman collection file (e.g., path_to_postman_collection.json).
- environment_file: Path to your Postman environment file (e.g., path_to_postman_environment.json).

# Run the script:
- `python script_name.py`

# Script Details
The script includes the following functions:

- load_postman_collection(file_path): Loads the Postman collection from the specified file.
- load_postman_environment(file_path): Loads the Postman environment from the specified file.
- resolve_variables(data, environment): Resolves variables in the request URL, headers, and body using the provided environment.
send_to_burp_repeater(request_data, burp_host, burp_port): Sends the resolved request to the Burp Suite Repeater.
