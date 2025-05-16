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

    def create(self, project_id: int, name: str, description: str,
               additional_params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Create a new knowledge base for a specific project.

        :param project_id: ID of the project to create the knowledge base in
        :param name: Knowledge base name
        :param description: Knowledge base description
        :param additional_params: Optional parameters including:
            - language (str): Language of the knowledge base (ISO 639-1 code, default: 'en')
            - sources (list): List of sources to index into the knowledge base
              Each source can be a dict with either 'url' or 'query' key:
              - {'url': 'https://example.com/doc'} for web sources
              - {'query': 'search query'} for search-based sources
        :return: Dictionary with created knowledge base details
        :raises: AuthenticationError if API key is invalid
        :raises: ValidationError if required parameters are missing
        :raises: AccessDeniedError if permission denied
        :raises: ResourceNotFoundError if project doesn't exist
        """
        data = {
            'projectId': project_id,
            'name': name,
            'description': description
        }

        if additional_params:
            data.update(additional_params)

        return self.client.request("POST", "knowledge-bases/create", data=data)

    def archive(self, knowledge_base_id: int) -> Dict[str, Any]:
        """
        Archives a knowledge base.

        :param knowledge_base_id: ID of the knowledge base to archive
        :return: Dictionary with updated knowledge base details
        :raises: AuthenticationError if API key is invalid
        :raises: AccessDeniedError if knowledge base doesn't exist or permission denied
        :raises: ResourceNotFoundError if knowledge base doesn't exist
        """
        endpoint = f"knowledge-bases/{knowledge_base_id}/archive"
        return self.client.request("PUT", endpoint)

    def unarchive(self, knowledge_base_id: int) -> Dict[str, Any]:
        """
        Removes a knowledge base from archived status.

        :param knowledge_base_id: ID of the knowledge base to unarchive
        :return: Dictionary with updated knowledge base details
        :raises: AuthenticationError if API key is invalid
        :raises: AccessDeniedError if knowledge base doesn't exist or permission denied
        :raises: ResourceNotFoundError if knowledge base doesn't exist
        """
        endpoint = f"knowledge-bases/{knowledge_base_id}/unarchive"
        return self.client.request("PUT", endpoint)