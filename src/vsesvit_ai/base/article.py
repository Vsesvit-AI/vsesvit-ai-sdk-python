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

    def create(self, project_id: int, name: str, brief: str,
               additional_params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Create a new article with flexible configuration options.

        :param project_id: ID of the project to create the article in
        :param name: Article title
        :param brief: Detailed description of what the article should cover
        :param additional_params: Optional parameters including:
            - requestWords (int): Requested word count for the article (default: 3000)
            - quality (str): Quality level for content generation (premium/standard)
            - country (str): ISO country code for region-specific content
            - language (str): ISO language code for content language (default: 'en')
            - website (str): Target website URL if applicable
            - temperature (str): AI creativity level (0.0-2.0) (default: '1.0')
            - imageModel (str): Model to use for image generation
            - imageOrientation (str): Orientation for generated images
            - useImages (bool): Whether to include images (default: True)
            - useQuotes (bool): Whether to include quotes (default: True)
            - useTables (bool): Whether to include tables (default: True)
            - useBulletLists (bool): Whether to include bullet lists (default: True)
            - useDiagrams (bool): Whether to include diagrams (default: True)
            - useTOC (bool): Whether to include table of contents (default: True)
            - useFAQ (bool): Whether to include FAQ section (default: True)
            - useAuthorInfo (bool): Whether to include author information (default: False)
            - useStrongTag (bool): Whether to use <strong> HTML tags (default: True)
            - useDelTag (bool): Whether to use <del> HTML tags (default: False)
            - useSubTag (bool): Whether to use <sub> HTML tags (default: False)
            - useSupTag (bool): Whether to use <sup> HTML tags (default: False)
            - useEmTag (bool): Whether to use <em> HTML tags (default: False)
            - useEmoji (bool): Whether to use emojis in content (default: False)
            - useProtection (bool): Whether to use AI detection protection (default: False)
            - allowAdditionalLinks (bool): Whether to allow extra links in content (default: False)
            - knowledgeIds (list): IDs of knowledge bases to use
            - authorId (int): ID of the author to use
            - audienceId (int): ID of the target audience
            - keywords (list): Keywords to include in article (list of dicts with 'value' and 'quantity')
            - rules (list): Writing style rules to follow (list of dicts with 'rule')
            - externalLinks (list): External links to include (list of dicts with 'url')
            - contentSources (list): Source URLs for content research (list of dicts with 'url')
            - sections (list): Article sections (null to let AI generate sections automatically)
        :return: Dictionary with created article details
        :raises: AuthenticationError if API key is invalid
        :raises: ValidationError if required parameters are missing
        :raises: AccessDeniedError if permission denied
        """
        data = {
            'projectId': project_id,
            'name': name,
            'brief': brief
        }

        if additional_params:
            data.update(additional_params)

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