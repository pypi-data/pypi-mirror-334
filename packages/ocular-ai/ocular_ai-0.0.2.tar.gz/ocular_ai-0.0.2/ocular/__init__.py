"""
Ocular AI Python SDK.

This is the main entry point for the Ocular SDK.
"""

import sys
from typing import Optional, Dict, Any

from ocular.core.workspace import Workspace
from ocular.api import OcularApiClient
from ocular.utils.config import OcularConfig
from ocular.utils.logging import setup_logging, get_logger
from ocular.utils.errors import OcularError, ValidationError

logger = get_logger()


class Ocular:
    """
    Main class for interacting with the Ocular AI platform.

    This is the primary entry point for the Ocular SDK. Use this class to
    access workspaces, projects, versions, and exports.
    """

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
        Initialize the Ocular SDK.

        Args:
            api_key (str, optional): Your Ocular AI API key. If not provided,
                will look for OCULAR_API_KEY environment variable.
            api_url (str, optional): The base URL for the Ocular API.
            timeout (int, optional): Request timeout in seconds.
            max_retries (int, optional): Maximum number of retries for failed requests.
            backoff_factor (float, optional): Backoff factor for retries.
            debug (bool, optional): Enable debug mode with verbose logging.

        Raises:
            ValidationError: If the API key is not provided and not found in environment variables
        """
        log_level = "DEBUG" if debug else "INFO"
        setup_logging(level=log_level)

        self.config = OcularConfig(
            api_key=api_key,
            api_url=api_url,
            timeout=timeout,
            max_retries=max_retries,
            backoff_factor=backoff_factor,
            debug=debug,
        )

        try:
            self.config.validate()

            self.api_client = OcularApiClient(
                api_key=self.config.api_key,
                base_url=self.config.api_url,
                timeout=self.config.timeout,
                max_retries=self.config.max_retries,
                backoff_factor=self.config.backoff_factor,
            )

            logger.debug("Ocular SDK initialized successfully")

        except ValidationError as e:
            logger.error(f"Failed to initialize Ocular SDK: {str(e)}")
            raise

    def workspace(self, workspace_id: str) -> Workspace:
        """
        Get a workspace by its ID.

        Args:
            workspace_id (str): The ID of the workspace

        Returns:
            Workspace: A workspace object

        Raises:
            OcularError: If the workspace cannot be retrieved
        """
        if not workspace_id:
            raise ValidationError("Workspace ID is required")

        logger.info(f"Accessing workspace: {workspace_id}")

        try:
            workspace_info = self.api_client.get_workspace(workspace_id)
            return Workspace(self.config.api_key, workspace_info)
        except OcularError as e:
            logger.error(f"Failed to retrieve workspace {workspace_id}: {str(e)}")
            raise
