"""
Configuration management for the Ocular SDK.
"""

import os
from typing import Optional, Dict, Any


class OcularConfig:
    """
    Configuration manager for the Ocular SDK.

    This class centralizes all configuration options for the SDK, including
    the API URL, API key, timeouts, retries, etc.
    """

    DEFAULT_API_URL = "https://staging.api.useocular.com/api/v1"
    DEFAULT_TIMEOUT = 300
    DEFAULT_MAX_RETRIES = 3
    DEFAULT_BACKOFF_FACTOR = 0.5

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
        timeout: Optional[int] = None,
        max_retries: Optional[int] = None,
        backoff_factor: Optional[float] = None,
        debug: bool = False,
    ):
        """
        Initialize the SDK configuration.

        Args:
            api_key (str, optional): The Ocular API key. If not provided, will look for OCULAR_API_KEY environment var.
            api_url (str, optional): The base URL for the Ocular API. Defaults to https://api.ocular.ai/v1.
            timeout (int, optional): Default request timeout in seconds. Defaults to 30.
            max_retries (int, optional): Maximum number of retries for failed requests. Defaults to 3.
            backoff_factor (float, optional): Backoff factor for retries. Defaults to 0.5.
            debug (bool, optional): Enable debug mode with verbose logging. Defaults to False.
        """
        self.api_key = api_key or os.environ.get("OCULAR_API_KEY")

        self.api_url = api_url or os.environ.get("OCULAR_API_URL", self.DEFAULT_API_URL)
        self.timeout = timeout or int(
            os.environ.get("OCULAR_TIMEOUT", self.DEFAULT_TIMEOUT)
        )
        self.max_retries = max_retries or int(
            os.environ.get("OCULAR_MAX_RETRIES", self.DEFAULT_MAX_RETRIES)
        )
        self.backoff_factor = backoff_factor or float(
            os.environ.get("OCULAR_BACKOFF_FACTOR", self.DEFAULT_BACKOFF_FACTOR)
        )
        self.debug = debug or os.environ.get("OCULAR_DEBUG", "").lower() in (
            "true",
            "1",
            "yes",
        )

    def validate(self) -> None:
        """
        Validate the configuration settings.

        Raises:
            ValueError: If required settings are missing or invalid
        """
        if not self.api_key:
            raise ValueError(
                "API key is required. Provide it in the constructor or set OCULAR_API_KEY environment variable."
            )

        if not self.api_url:
            raise ValueError("API URL is required.")

        if self.timeout <= 0:
            raise ValueError("Timeout must be greater than 0.")

        if self.max_retries < 0:
            raise ValueError("Max retries cannot be negative.")

        if self.backoff_factor < 0:
            raise ValueError("Backoff factor cannot be negative.")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the config to a dictionary.

        Returns:
            Dict[str, Any]: The config as a dictionary
        """
        return {
            "api_url": self.api_url,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
            "backoff_factor": self.backoff_factor,
            "debug": self.debug,
        }

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "OcularConfig":
        """
        Create a config instance from a dictionary.

        Args:
            config_dict (Dict[str, Any]): The config dictionary

        Returns:
            OcularConfig: The config instance
        """
        return cls(
            api_key=config_dict.get("api_key"),
            api_url=config_dict.get("api_url"),
            timeout=config_dict.get("timeout"),
            max_retries=config_dict.get("max_retries"),
            backoff_factor=config_dict.get("backoff_factor"),
            debug=config_dict.get("debug", False),
        )
