from typing import Optional, Dict, Any, List
from ocular.core.version import Version
from ocular.api import OcularApiClient
from ocular.utils.logging import get_logger

logger = get_logger()


class Project:
    """
    Represents a project in the Ocular AI platform.
    """

    def __init__(self, project_info: Dict[str, Any], api_key: str):
        """
        Initialize a project instance.

        Args:
            project_info (Dict[str, Any]): Project information dictionary
            api_key (str): Ocular AI API key
        """
        if not api_key:
            raise ValueError("API key is required")
        self.api_key = api_key
        self.id = project_info["id"]
        self.name = project_info.get("name", "")
        self.description = project_info.get("description", "")

        self.api_client = OcularApiClient(api_key)

    def version(self, version_id: str) -> Version:
        """
        Get a specific version of the project.

        Args:
            version_id (str): The version ID to retrieve

        Returns:
            Version: A version object
        """
        logger.debug(f"Getting version {version_id} for project: {self.id}")
        version_info = self.api_client.get_version(self.id, version_id)
        return Version(version_info, self.api_key)

    def list_versions(self) -> List[Version]:
        """
        List all versions of the project.

        Returns:
            List[Version]: List of version objects
        """
        logger.debug(f"Listing versions for project: {self.id}")
        versions_info = self.api_client.get_project_versions(self.id)
        return [Version(version_info, self.api_key) for version_info in versions_info]
