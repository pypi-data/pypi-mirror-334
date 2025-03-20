"""
Core API client for the Ocular SDK.

This module provides the main API client for interacting with the Ocular API.
"""

import logging
from typing import Dict, Any, List, Optional

from ocular.utils.http_client import HttpClient
from ocular.utils.errors import OcularError
from ocular.utils.logging import get_logger
from ocular.config import OCULAR_API_URL
import requests

logger = get_logger()


class OcularApiClient(HttpClient):
    """
    Main API client for the Ocular API.

    This class handles all API requests to the Ocular API and provides
    methods for accessing workspaces, projects, versions, and exports.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = OCULAR_API_URL,
        timeout: int = 300,
        max_retries: int = 3,
        backoff_factor: float = 0.5,
    ):
        """
        Initialize the Ocular API client.

        Args:
            api_key (str): The Ocular API key
            base_url (str, optional): The base URL for the Ocular API. Defaults to OCULAR_API_URL.
            timeout (int, optional): Request timeout in seconds. Defaults to 30.
            max_retries (int, optional): Maximum number of retries. Defaults to 3.
            backoff_factor (float, optional): Backoff factor for retries. Defaults to 0.5.
        """
        super().__init__(api_key, base_url, timeout, max_retries, backoff_factor)
        logger.debug(f"Initialized Ocular API client with base URL: {base_url}")

    def get_workspace(self, workspace_id: str) -> Dict[str, Any]:
        """
        Get information about a workspace.

        Args:
            workspace_id (str): The ID of the workspace

        Returns:
            Dict[str, Any]: Workspace information

        Raises:
            OcularError: If the request fails
        """
        logger.debug(f"Getting workspace with ID: {workspace_id}")
        return self.get(f"workspaces/{workspace_id}")

    def get_project(self, workspace_id: str, project_id: str) -> Dict[str, Any]:
        """
        Get information about a project in a workspace.

        Args:
            workspace_id (str): The ID of the workspace
            project_id (str): The ID of the project

        Returns:
            Dict[str, Any]: Project information

        Raises:
            OcularError: If the request fails
        """
        logger.debug(
            f"Getting project with ID: {project_id} in workspace: {workspace_id}"
        )
        return self.get(f"workspaces/{workspace_id}/projects/{project_id}")

    def get_version(self, project_id: str, version_id: str) -> Dict[str, Any]:
        """
        Get information about a version of a project.

        Args:
            project_id (str): The ID of the project
            version_id (str): The ID of the version

        Returns:
            Dict[str, Any]: Version information

        Raises:
            OcularError: If the request fails
        """
        logger.debug(f"Getting version with ID: {version_id} in project: {project_id}")
        return self.get(f"projects/{project_id}/versions/{version_id}")

    def get_project_versions(self, project_id: str) -> List[Dict[str, Any]]:
        """
        Get all versions of a project.

        Args:
            project_id (str): The ID of the project

        Returns:
            List[Dict[str, Any]]: List of versions

        Raises:
            OcularError: If the request fails
        """
        logger.debug(f"Getting all versions for project: {project_id}")
        return self.get(f"projects/{project_id}/versions")

    def download_export(self, version_id: str, export_id: str, stream: bool = False):
        """
        Download an export from a version.

        Args:
            version_id: ID of the version
            export_id: ID of the export
            stream: If True, returns the raw response object for streaming
                   If False, returns the content as bytes (default)

        Returns:
            Either the response object (for streaming) or the file content (bytes)
        """
        endpoint = f"versions/{version_id}/exports/{export_id}"

        if stream:
            url = f"{self.base_url}/{endpoint}"
            response = self.session.get(url, stream=True, timeout=self.timeout)
            response.raise_for_status()
            return response
        else:
            response_data, status_code = self._make_request("GET", endpoint)
            return response_data

    def get_version_exports(
        self, project_id: str, version_id: str, headers: Optional[Dict[str, str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all exports for a specific version

        Args:
            version_id (str): The ID of the version
            headers (dict, optional): HTTP headers for the request

        Returns:
            dict: The exports data

        Raises:
            OcularAuthError: If authentication fails
            OcularResourceNotFoundError: If the version is not found
            OcularAPIError: For other API errors
        """
        try:
            response = self.session.get(
                f"{self.base_url}/projects/{project_id}/versions/{version_id}/exports",
                headers=headers,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get version exports: {e}")
            raise OcularError(f"Failed to get version exports: {e}")

    def get_version_export(
        self,
        project_id: str,
        version_id: str,
        export_id: str,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Get a specific export from a version

        Args:
            version_id (str): The ID of the version
            export_id (str): The ID of the export
            headers (dict, optional): HTTP headers for the request

        Returns:
            dict: The export data

        Raises:
            OcularAuthError: If authentication fails
            OcularResourceNotFoundError: If the version or export is not found
            OcularAPIError: For other API errors
        """
        try:
            response = self.session.get(
                f"{self.base_url}/projects/{project_id}/versions/{version_id}/exports/{export_id}",
                headers=headers,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get version export: {e}")
            raise OcularError(f"Failed to get version export: {e}")
