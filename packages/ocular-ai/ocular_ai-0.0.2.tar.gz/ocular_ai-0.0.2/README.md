# Ocular AI Python SDK

Official Python SDK for interacting with the Ocular AI Platform.

## Installation

```bash
pip install ocular
```

## Quick Start

```python
from ocular import Ocular

# Initialize the SDK with your API key
ocular = Ocular(api_key="your_api_key_here")

# Access a workspace
workspace = ocular.workspace("your_workspace_id")

# Get a project from the workspace
project = workspace.project("your_project_id")

# Get a version from the project
version = project.version("your_version_id")

# Get an export from the version
export = version.export("your_export_id")

# Download the export dataset
dataset_path = export.download()
print(f"Downloaded export to: {dataset_path}")
```

## Configuration

The SDK can be configured using the following parameters:

```python
ocular = Ocular(
    api_key="your_api_key",  # Required unless OCULAR_API_KEY env var is set
    api_url="https://api.ocular.ai/v1",  # Optional custom API URL
    timeout=30,  # Request timeout in seconds
    max_retries=3,  # Maximum number of retries for failed requests
    backoff_factor=0.5,  # Backoff factor for retries
    debug=False,  # Enable debug logging
)
```

You can also configure the SDK using environment variables:

- `OCULAR_API_KEY`: Your Ocular API key
- `OCULAR_API_URL`: The base URL for the Ocular API
- `OCULAR_TIMEOUT`: Default request timeout in seconds
- `OCULAR_MAX_RETRIES`: Maximum number of retries for failed requests
- `OCULAR_BACKOFF_FACTOR`: Backoff factor for retries
- `OCULAR_DEBUG`: Enable debug mode (set to "true", "1", or "yes")
- `OCULAR_LOG_LEVEL`: Set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

## Error Handling

The SDK uses a structured error hierarchy for different types of errors:

```python
from ocular.utils.errors import (
    OcularError,  # Base exception for all errors
    AuthenticationError,  # Authentication issues
    ValidationError,  # Invalid parameters
    ResourceNotFoundError,  # Resource not found
    RateLimitError,  # API rate limits exceeded
    ServerError,  # Server-side errors
    NetworkError,  # Network connectivity issues
    TimeoutError,  # Request timed out
)

try:
    workspace = ocular.workspace("invalid_id")
except ResourceNotFoundError as e:
    print(f"Workspace not found: {e}")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except OcularError as e:
    print(f"An error occurred: {e}")
```

## Logging

The SDK uses Python's standard logging library. You can configure logging using:

```python
from ocular.utils.logging import setup_logging

# Setup logging with custom settings
logger = setup_logging(
    level="DEBUG",
    log_file="ocular.log",  # Optional file to log to
)
```
