from typing import Dict, Any


class Author:
    def __init__(self, client):
        """
        Initialize the Author resource

        :param client: VsesvitAI client instance
        """
        self.client = client

    def get_list(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Get a list of authors with pagination and filtering options.

        :param params: Query parameters for filtering and pagination
        :return: Dictionary with authors list and pagination info
        :raises: AuthenticationError if API key is invalid
        :raises: AccessDeniedError if permission denied
        :raises: ValidationError if query parameters are invalid
        """
        return self.client.request("GET", "authors", params=params)

    def get_by_id(self, author_id: int) -> Dict[str, Any]:
        """
        Returns detailed information about a specific author.

        :param author_id: ID of the author to retrieve
        :return: Dictionary with author details
        :raises: AuthenticationError if API key is invalid
        :raises: AccessDeniedError if author doesn't exist or permission denied
        :raises: ResourceNotFoundError if author doesn't exist
        """
        return self.client.request("GET", f"authors/{author_id}")

    def create(self, project_id: int, name: str, biography: str,
               additional_params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Create a new author for a specific project.

        :param project_id: ID of the project to create the author in
        :param name: Author name
        :param biography: Author biography
        :param additional_params: Optional parameters including:
            - ppm (dict): Author persona parameters (e.g., writing style, tone, expertise)
            - sources (list): List of source URLs for training the author's writing style
              Each source should be a dict with 'url' key
        :return: Dictionary with created author details
        :raises: AuthenticationError if API key is invalid
        :raises: ValidationError if required parameters are missing
        :raises: AccessDeniedError if permission denied
        :raises: ResourceNotFoundError if project doesn't exist
        """
        data = {
            'projectId': project_id,
            'name': name,
            'biography': biography
        }

        if additional_params:
            data.update(additional_params)

        return self.client.request("POST", "authors/create", data=data)

    def archive(self, author_id: int) -> Dict[str, Any]:
        """
        Archives an author.

        :param author_id: ID of the author to archive
        :return: Dictionary with updated author details
        :raises: AuthenticationError if API key is invalid
        :raises: AccessDeniedError if author doesn't exist or permission denied
        :raises: ResourceNotFoundError if author doesn't exist
        """
        endpoint = f"authors/{author_id}/archive"
        return self.client.request("PUT", endpoint)

    def unarchive(self, author_id: int) -> Dict[str, Any]:
        """
        Removes an author from archived status.

        :param author_id: ID of the author to unarchive
        :return: Dictionary with updated author details
        :raises: AuthenticationError if API key is invalid
        :raises: AccessDeniedError if author doesn't exist or permission denied
        :raises: ResourceNotFoundError if author doesn't exist
        """
        endpoint = f"authors/{author_id}/unarchive"
        return self.client.request("PUT", endpoint)