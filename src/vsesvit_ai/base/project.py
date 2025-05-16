from typing import Dict, Any, Optional, Union


class Project:
    def __init__(self, client):
        """
        Initialize the Project resource

        :param client: VsesvitAI client instance
        """
        self.client = client

    def get_list(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Get a list of projects with pagination and filtering options.

        :param params: Query parameters for filtering and pagination
        :return: Dictionary with projects list and pagination info
        :raises: AuthenticationError if API key is invalid
        :raises: AccessDeniedError if permission denied
        :raises: ValidationError if query parameters are invalid
        """
        return self.client.request("GET", "projects", params=params)

    def get_by_id(self, project_id: int) -> Dict[str, Any]:
        """
        Returns detailed information about a specific project.

        :param project_id: ID of the project to retrieve
        :return: Dictionary with project details
        :raises: AuthenticationError if API key is invalid
        :raises: AccessDeniedError if project doesn't exist or permission denied
        :raises: ResourceNotFoundError if project doesn't exist
        """

        return self.client.request("GET", f"projects/{project_id}")

    def create(self, name: str, description: str,
               additional_params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Create a new project with flexible configuration options.

        :param name: Project name
        :param description: Detailed description of the project
        :param additional_params: Optional parameters (if any additional ones exist)
        :return: Dictionary with created project details
        :raises: AuthenticationError if API key is invalid
        :raises: ValidationError if required parameters are missing
        :raises: AccessDeniedError if permission denied
        """
        data = {
            'name': name,
            'description': description
        }

        if additional_params:
            data.update(additional_params)

        return self.client.request("POST", "projects/create", data=data)

    def archive(self, project_id: int) -> Dict[str, Any]:
        """
        Archives a project.

        :param project_id: ID of the project to archive
        :return: Dictionary with updated project details
        :raises: AuthenticationError if API key is invalid
        :raises: AccessDeniedError if project doesn't exist or permission denied
        :raises: ResourceNotFoundError if project doesn't exist
        """
        endpoint = f"projects/{project_id}/archive"
        return self.client.request("PUT", endpoint)

    def unarchive(self, project_id: int) -> Dict[str, Any]:
        """
        Removes a project from archived status.

        :param project_id: ID of the project to unarchive
        :return: Dictionary with updated project details
        :raises: AuthenticationError if API key is invalid
        :raises: AccessDeniedError if project doesn't exist or permission denied
        :raises: ResourceNotFoundError if project doesn't exist
        """
        endpoint = f"projects/{project_id}/unarchive"
        return self.client.request("PUT", endpoint)