# Postman2Burp
This script allows you to import Postman API collections into Burp Suite, send the requests to the Repeater, and handle variable resolution.

# Features
- Load Postman Collection: Reads a Postman collection JSON file.
- Load Postman Environment: Reads a Postman environment JSON file.
- Resolve Variables: Replaces variables in the request URL, headers, and body with actual values from the environment.
- Send Requests to Burp Suite Repeater: Uses Burp Suite's API to send the resolved requests to the Repeater.

# Installation
- Clone the repository
- `pip install requests`

## Usage

### Prerequisites
- Python 3.x installed.
- Required Python packages installed (`requests`, `argparse`).

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/crynomore/postman2burp
2. Navigate to the project directory
### Running the Script
To send requests from a Postman collection:
```bash
python main.py path_to_your_postman_collection.json [--environment path_to_your_postman_environment.json]
```

Replace path_to_your_postman_collection.json and path_to_your_postman_environment.json with the actual paths to your Postman collection and optional environment file.

If no environment file is provided, the script runs without it.
Ensure all necessary variables (baseUrl, etc.) are defined in your environment file for proper request handling.

# Script Details
The script includes the following functions:

- load_postman_collection(file_path): Loads the Postman collection from the specified file.
- load_postman_environment(file_path): Loads the Postman environment from the specified file.
- resolve_variables(data, environment): Resolves variables in the request URL, headers, and body using the provided environment.
send_to_burp_repeater(request_data, burp_host, burp_port): Sends the resolved request to the Burp Suite Repeater.
