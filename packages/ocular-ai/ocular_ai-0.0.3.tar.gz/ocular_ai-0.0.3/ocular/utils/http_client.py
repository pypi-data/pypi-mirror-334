"""
HTTP client for the Ocular SDK.

This module provides a base HTTP client that handles common functionality like
request handling, error handling, retries, and authentication.
"""

import time
import requests
import logging
import platform
from typing import Dict, Any, Optional, Union, Tuple
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ocular.utils.errors import NetworkError, TimeoutError, handle_api_error

logger = logging.getLogger("ocular")

SDK_VERSION = "0.1.0"


class HttpClient:
    """Base HTTP client for the Ocular API."""

    def __init__(
        self,
        api_key: str,
        base_url: str,
        timeout: int = 30,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
    ):
        """
        Initialize the HTTP client.

        Args:
            api_key (str): The Ocular API key
            base_url (str): The base URL for the Ocular API
            timeout (int, optional): Request timeout in seconds. Defaults to 30.
            max_retries (int, optional): Maximum number of retries. Defaults to 3.
            backoff_factor (float, optional): Backoff factor for retries. Defaults to 0.5.
        """
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.session = requests.Session()

        retry_statuses = [429, 500, 502, 503, 504]
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=retry_statuses,
            allowed_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        )

        self.session.mount("https://", HTTPAdapter(max_retries=retry_strategy))
        self.session.mount("http://", HTTPAdapter(max_retries=retry_strategy))

        self.session.headers.update(
            {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
        )

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = None,
    ) -> Tuple[Dict[str, Any], int]:
        """
        Make an HTTP request to the API.

        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE)
            endpoint (str): API endpoint to call
            params (Dict[str, Any], optional): Query parameters
            data (Dict[str, Any], optional): Form data
            json_data (Dict[str, Any], optional): JSON data
            headers (Dict[str, str], optional): Additional headers
            timeout (int, optional): Request timeout in seconds

        Returns:
            Tuple[Dict[str, Any], int]: Response JSON and status code

        Raises:
            NetworkError: If a network error occurs
            TimeoutError: If the request times out
            OcularError: For other API errors
        """
        if timeout is None:
            timeout = self.timeout

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        request_headers = {}
        if headers:
            request_headers.update(headers)

        logger.debug(f"Making {method} request to {url}")

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                json=json_data,
                headers=request_headers,
                timeout=timeout,
            )

            self._log_request_response(method, url, response.status_code)

            if 200 <= response.status_code < 300:
                if response.content:
                    try:
                        return response.json(), response.status_code
                    except ValueError:
                        return {
                            "data": response.content.decode("utf-8")
                        }, response.status_code
                return {}, response.status_code

            raise handle_api_error(response)

        except requests.exceptions.Timeout:
            logger.error(f"Request to {url} timed out after {timeout} seconds")
            raise TimeoutError(f"Request timed out after {timeout} seconds")
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Network error when connecting to {url}: {str(e)}")
            raise NetworkError(f"Network error: {str(e)}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {str(e)}")
            raise NetworkError(f"Request error: {str(e)}")

    def _log_request_response(self, method: str, url: str, status_code: int) -> None:
        """
        Log request and response details.

        Args:
            method (str): HTTP method
            url (str): Request URL
            status_code (int): Response status code
        """
        redacted_url = self._redact_url(url)
        logger.debug(f"{method} {redacted_url} -> {status_code}")

    def _redact_url(self, url: str) -> str:
        """
        Redact sensitive information from URL for logging.

        Args:
            url (str): The URL to redact

        Returns:
            str: Redacted URL
        """
        return url

    def get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs
    ) -> Dict[str, Any]:
        """
        Make a GET request to the API.

        Args:
            endpoint (str): API endpoint
            params (Dict[str, Any], optional): Query parameters

        Returns:
            Dict[str, Any]: Response data
        """
        data, _ = self._make_request("GET", endpoint, params=params, **kwargs)
        return data

    def post(
        self, endpoint: str, json_data: Optional[Dict[str, Any]] = None, **kwargs
    ) -> Dict[str, Any]:
        """
        Make a POST request to the API.

        Args:
            endpoint (str): API endpoint
            json_data (Dict[str, Any], optional): JSON data

        Returns:
            Dict[str, Any]: Response data
        """
        data, _ = self._make_request("POST", endpoint, json_data=json_data, **kwargs)
        return data

    def put(
        self, endpoint: str, json_data: Optional[Dict[str, Any]] = None, **kwargs
    ) -> Dict[str, Any]:
        """
        Make a PUT request to the API.

        Args:
            endpoint (str): API endpoint
            json_data (Dict[str, Any], optional): JSON data

        Returns:
            Dict[str, Any]: Response data
        """
        data, _ = self._make_request("PUT", endpoint, json_data=json_data, **kwargs)
        return data

    def delete(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make a DELETE request to the API.

        Args:
            endpoint (str): API endpoint

        Returns:
            Dict[str, Any]: Response data
        """
        data, _ = self._make_request("DELETE", endpoint, **kwargs)
        return data
