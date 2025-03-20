# GCP MCP Server

An MCP server that provides tools for interacting with Google Cloud Platform Cloud Functions, specifically for retrieving logs.

## Features

- Retrieve logs from GCP Cloud Functions
- Supports both stdio and SSE transport modes
- Easy integration with MCP clients
- Flexible authentication options:
  - Service Account JSON key file
  - Interactive authentication (Application Default Credentials)

## Installation

```bash
pip install gcp-mcp-server
```

## Prerequisites

1. Google Cloud SDK installed and configured
2. Appropriate GCP permissions to access Cloud Functions and Cloud Logging
3. Python 3.10 or higher
4. Authentication set up (see Authentication section below)

## Authentication

The server supports two authentication methods:

### 1. Service Account JSON Key

You can provide a service account JSON key file in two ways:
```bash
# Option 1: Command line argument
gcp-mcp-server --service-account ~/path/to/service-account.json

# Option 2: Environment variable
export GCP_SERVICE_ACCOUNT_PATH=~/path/to/service-account.json
gcp-mcp-server
```

### 2. Application Default Credentials (Interactive)

If no service account is provided, the server will use Application Default Credentials:
1. Run `gcloud auth application-default login`
2. Follow the interactive authentication process
3. Start the server normally:
```bash
gcp-mcp-server
```

## Usage

### Starting the server

Using stdio transport (default):
```bash
gcp-mcp-server
```

Using SSE transport:
```bash
gcp-mcp-server --transport sse --port 8000
```

### Available Tools

#### get_function_logs

Retrieves logs for a specified Cloud Function.

Parameters:
- `project_id`: The GCP project ID
- `function_name`: The name of the Cloud Function
- `minutes`: Number of minutes of logs to retrieve (default: 10)
- `filter`: Optional additional filter for the logs

## Development

1. Clone the repository
2. Install dependencies:
```bash
pip install -e .
```

## Troubleshooting

### Authentication Issues

1. If using a service account:
   - Ensure the JSON key file exists and is readable
   - Verify the service account has the necessary permissions (roles/logging.viewer at minimum)
   - Check the file path is correct

2. If using application default credentials:
   - Run `gcloud auth application-default login` again
   - Verify you're logged into the correct account with `gcloud auth list`
   - Ensure your account has the necessary permissions

## License

MIT License
