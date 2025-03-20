"""
Error classes for the Ocular SDK.

This module contains all the exceptions that can be raised by the Ocular SDK.
"""


class OcularError(Exception):
    """Base exception for all Ocular SDK errors."""

    def __init__(self, message=None, http_status=None, request_id=None, response=None):
        self.message = message
        self.http_status = http_status
        self.request_id = request_id
        self.response = response

        error_message = message
        if http_status:
            error_message = f"{message} (HTTP {http_status})"
        if request_id:
            error_message = f"{error_message}, Request ID: {request_id}"

        super().__init__(error_message)


class AuthenticationError(OcularError):
    """Raised when authentication fails, typically due to invalid API key."""

    pass


class NetworkError(OcularError):
    """Raised for network connectivity issues."""

    pass


class ValidationError(OcularError):
    """Raised when parameters or inputs fail validation."""

    pass


class ResourceNotFoundError(OcularError):
    """Raised when a requested resource (workspace, project, etc.) is not found."""

    pass


class RateLimitError(OcularError):
    """Raised when API rate limits are exceeded."""

    pass


class ServerError(OcularError):
    """Raised for server-side errors (5xx responses)."""

    pass


class TimeoutError(OcularError):
    """Raised when a request times out."""

    pass


def handle_api_error(response):
    """
    Convert an HTTP error response into the appropriate OcularError subclass.

    Args:
        response: The HTTP response object from requests

    Returns:
        An appropriate OcularError subclass
    """
    status_code = response.status_code
    request_id = response.headers.get("Request-ID")

    try:
        error_data = response.json()
        message = error_data.get(
            "message", error_data.get("error", "Unknown API error")
        )
    except (ValueError, KeyError):
        message = f"API error with status code: {status_code}"

    # Select appropriate error class based on status code
    if status_code == 401:
        return AuthenticationError(message, status_code, request_id, response)
    elif status_code == 404:
        return ResourceNotFoundError(message, status_code, request_id, response)
    elif status_code == 422:
        return ValidationError(message, status_code, request_id, response)
    elif status_code == 429:
        return RateLimitError(message, status_code, request_id, response)
    elif 500 <= status_code < 600:
        return ServerError(message, status_code, request_id, response)
    else:
        return OcularError(message, status_code, request_id, response)
