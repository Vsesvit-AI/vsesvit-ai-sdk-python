from typing import Dict, Any


class Audience:
    def __init__(self, client):
        """
        Initialize the Audience resource

        :param client: VsesvitAI client instance
        """
        self.client = client

    def get_list(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Get a list of audiences with pagination and filtering options.

        :param params: Query parameters for filtering and pagination
        :return: Dictionary with audiences list and pagination info
        :raises: AuthenticationError if API key is invalid
        :raises: AccessDeniedError if permission denied
        :raises: ValidationError if query parameters are invalid
        """
        return self.client.request("GET", "audiences", params=params)

    def get_by_id(self, audience_id: int) -> Dict[str, Any]:
        """
        Returns detailed information about a specific audience.

        :param audience_id: ID of the audience to retrieve
        :return: Dictionary with audience details
        :raises: AuthenticationError if API key is invalid
        :raises: AccessDeniedError if audience doesn't exist or permission denied
        :raises: ResourceNotFoundError if audience doesn't exist
        """
        return self.client.request("GET", f"audiences/{audience_id}")