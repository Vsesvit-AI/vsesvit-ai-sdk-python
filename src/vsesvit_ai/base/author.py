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