from typing import Dict, Any, Optional, Union


class Article:
    def __init__(self, client):
        """
        Initialize the Articles resource

        :param client: VsesvitAI client instance
        """
        self.client = client

    def get_list(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Get a list of articles with pagination and filtering options.

        :param params: Query parameters for filtering and pagination
        :return: Dictionary with articles list and pagination info
        :raises: AuthenticationError if API key is invalid
        :raises: AccessDeniedError if permission denied
        :raises: ValidationError if query parameters are invalid
        """
        return self.client.request("GET", "articles", params=params)

    def get_by_id(self, article_id: int) -> Dict[str, Any]:
        """
        Returns detailed information about a specific article.

        :param article_id: ID of the article to retrieve
        :return: Dictionary with article details
        :raises: AuthenticationError if API key is invalid
        :raises: AccessDeniedError if article doesn't exist or permission denied
        :raises: ResourceNotFoundError if article doesn't exist
        """
        return self.client.request("GET", f"articles/{article_id}")

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new article with flexible configuration options.

        :param data: Article creation parameters
        :return: Dictionary with created article details
        :raises: AuthenticationError if API key is invalid
        :raises: ValidationError if required parameters are missing
        :raises: AccessDeniedError if permission denied
        """
        return self.client.request("POST", "articles/create", data=data)

    def download(self, article_id: int, file_format: str, path: Optional[str] = None) -> Union[bytes, str]:
        """
        Downloads the article in the requested format.

        :param article_id: ID of the article to download
        :param file_format: Format to download (e.g., 'pdf', 'docx')
        :param path: Optional file path to save the downloaded file
        :return: File content as bytes or path string if path is provided
        :raises: AuthenticationError if API key is invalid
        :raises: AccessDeniedError if article doesn't exist or permission denied
        :raises: ValidationError if format is invalid
        :raises: ResourceNotFoundError if article doesn't exist
        """
        endpoint = f"articles/{article_id}/download/{file_format}"
        headers = {'accept': 'application/octet-stream'}
        content = self.client.request("GET", endpoint, headers=headers, return_json=False)
        if path:
            with open(path, 'wb') as file:
                file.write(content)
            return path
        else:
            return content

    def archive(self, article_id: int) -> Dict[str, Any]:
        """
        Archives an article.

        :param article_id: ID of the article to archive
        :return: Dictionary with updated article details
        :raises: AuthenticationError if API key is invalid
        :raises: AccessDeniedError if article doesn't exist or permission denied
        :raises: ResourceNotFoundError if article doesn't exist
        """
        endpoint = f"articles/{article_id}/archive"
        return self.client.request("PUT", endpoint)

    def unarchive(self, article_id: int) -> Dict[str, Any]:
        """
        Removes an article from archived status.

        :param article_id: ID of the article to unarchive
        :return: Dictionary with updated article details
        :raises: AuthenticationError if API key is invalid
        :raises: AccessDeniedError if article doesn't exist or permission denied
        :raises: ResourceNotFoundError if article doesn't exist
        """
        endpoint = f"articles/{article_id}/unarchive"
        return self.client.request("PUT", endpoint)
