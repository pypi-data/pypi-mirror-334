"""
Workspace module for the Ocular SDK.

This module provides the Workspace class for interacting with Ocular workspaces.
"""

import logging
from typing import List, Dict, Any, Optional

from ocular.core.project import Project
from ocular.api import OcularApiClient
from ocular.utils.errors import ValidationError
from ocular.utils.logging import get_logger
from ocular.config import OCULAR_API_URL

logger = get_logger()


class Workspace:
    """
    Manage an Ocular workspace.

    A workspace contains projects and other resources that are shared within
    a team or organization.
    """

    def __init__(self, api_key: str, workspace_info: Dict[str, Any]):
        """
        Initialize a workspace instance.

        Args:
            api_key (str): The Ocular API key
            workspace_info (Dict[str, Any]): Workspace information from the API

        Raises:
            ValidationError: If api_key is missing or workspace_info is invalid
        """
        if not api_key:
            raise ValidationError("A valid API key is required.")

        if not workspace_info or not isinstance(workspace_info, dict):
            raise ValidationError("Invalid workspace information provided.")

        self.api_key = api_key
        self.api_client = OcularApiClient(api_key)

        self.id = workspace_info.get("id")
        self.name = workspace_info.get("name")
        self.description = workspace_info.get("description")
        self.project_list = workspace_info.get("projects", [])

        if not self.id:
            raise ValidationError("Workspace information is missing ID.")

        logger.debug(f"Initialized workspace: {self.name} ({self.id})")

    def list_projects(self) -> List[Dict[str, Any]]:
        """
        List all projects in the workspace.

        Returns:
            List[Dict[str, Any]]: List of project information dictionaries
        """
        logger.debug(f"Listing projects in workspace: {self.id}")
        return self.project_list

    def projects(self) -> List[Project]:
        """
        Get all projects in the workspace as Project objects.

        Returns:
            List[Project]: List of Project objects
        """
        logger.debug(f"Getting all project objects in workspace: {self.id}")
        projects_array = []
        for project_info in self.project_list:
            proj = Project(project_info, self.api_key)
            projects_array.append(proj)
        return projects_array

    def project(self, project_id: str) -> Project:
        """
        Retrieve a Project object by its ID.

        Args:
            project_id (str): ID of the project

        Returns:
            Project: A Project object

        Raises:
            ValidationError: If the project ID is invalid
            OcularError: If the project cannot be retrieved
        """
        if not project_id:
            raise ValidationError("Project ID is required")

        if "/" in project_id:
            raise ValidationError(
                f"Invalid project ID format: {project_id}. IDs should not contain '/'."
            )

        logger.info(f"Retrieving project {project_id} from workspace {self.id}")

        project_info = self.api_client.get_project(self.id, project_id)

        logger.debug(
            f"Retrieved project: {project_info.get('name', 'Unnamed')} ({project_id})"
        )
        return Project(project_info, self.api_key)
