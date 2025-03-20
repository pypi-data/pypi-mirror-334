"""
Utility functions and classes for the Ocular SDK.
"""

from ocular.utils.errors import (
    OcularError,
    AuthenticationError,
    NetworkError,
    ValidationError,
    ResourceNotFoundError,
    RateLimitError,
    ServerError,
    TimeoutError,
    handle_api_error,
)

__all__ = [
    "OcularError",
    "AuthenticationError",
    "NetworkError",
    "ValidationError",
    "ResourceNotFoundError",
    "RateLimitError",
    "ServerError",
    "TimeoutError",
    "handle_api_error",
]
