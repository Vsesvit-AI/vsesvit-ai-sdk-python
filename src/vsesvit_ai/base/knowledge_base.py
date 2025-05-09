from typing import Dict, Any


class KnowledgeBase:
    def __init__(self, client):
        """
        Initialize the KnowledgeBase resource

        :param client: VsesvitAI client instance
        """
        self.client = client

    def get_list(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Get a list of knowledge bases with pagination and filtering options.

        :param params: Query parameters for filtering and pagination
        :return: Dictionary with knowledge bases list and pagination info
        :raises: AuthenticationError if API key is invalid
        :raises: AccessDeniedError if permission denied
        :raises: ValidationError if query parameters are invalid
        """
        return self.client.request("GET", "knowledge-bases", params=params)

    def get_by_id(self, knowledge_base_id: int) -> Dict[str, Any]:
        """
        Returns detailed information about a specific knowledge base.

        :param knowledge_base_id: ID of the knowledge base to retrieve
        :return: Dictionary with knowledge base details
        :raises: AuthenticationError if API key is invalid
        :raises: AccessDeniedError if knowledge base doesn't exist or permission denied
        :raises: ResourceNotFoundError if knowledge base doesn't exist
        """
        return self.client.request("GET", f"knowledge-bases/{knowledge_base_id}")