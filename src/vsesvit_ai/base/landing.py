from typing import Dict, Any, Optional, Union


class Landing:
    def __init__(self, client):
        """
        Initialize the Landings resource

        :param client: VsesvitAI client instance
        """
        self.client = client

    def get_list(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Get a list of landings with pagination and filtering options.

        :param params: Query parameters for filtering and pagination
        :return: Dictionary with landings list and pagination info
        :raises: AuthenticationError if API key is invalid
        :raises: AccessDeniedError if permission denied
        :raises: ValidationError if query parameters are invalid
        """
        return self.client.request("GET", "landings", params=params)

    def get_by_id(self, landing_id: int) -> Dict[str, Any]:
        """
        Returns detailed information about a specific landing.

        :param landing_id: ID of the landing to retrieve
        :return: Dictionary with landing details
        :raises: AuthenticationError if API key is invalid
        :raises: AccessDeniedError if landing doesn't exist or permission denied
        :raises: ResourceNotFoundError if landing doesn't exist
        """
        return self.client.request("GET", f"landings/{landing_id}")

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new landing with flexible configuration options.

        :param data: Landing creation parameters
        :return: Dictionary with created landing details
        :raises: AuthenticationError if API key is invalid
        :raises: ValidationError if required parameters are missing
        :raises: AccessDeniedError if permission denied
        """
        return self.client.request("POST", "landings/create", data=data)

    def download(self, landing_id: int, path: Optional[str] = None) -> Union[bytes, str]:
        """
        Downloads the landing in ZIP format.

        :param landing_id: ID of the landing to download
        :param path: Optional file path to save the downloaded file
        :return: File content as bytes or path string if path is provided
        :raises: AuthenticationError if API key is invalid
        :raises: AccessDeniedError if landing doesn't exist or permission denied
        :raises: ResourceNotFoundError if landing doesn't exist
        """
        endpoint = f"landings/{landing_id}/download"
        headers = {'accept': 'application/octet-stream'}
        content = self.client.request("GET", endpoint, headers=headers, return_json=False)

        if path:
            with open(path, 'wb') as file:
                file.write(content)
            return path
        else:
            return content

    def archive(self, landing_id: int) -> Dict[str, Any]:
        """
        Archives a landing.

        :param landing_id: ID of the landing to archive
        :return: Dictionary with updated landing details
        :raises: AuthenticationError if API key is invalid
        :raises: AccessDeniedError if landing doesn't exist or permission denied
        :raises: ResourceNotFoundError if landing doesn't exist
        """
        endpoint = f"landings/{landing_id}/archive"
        return self.client.request("PUT", endpoint)

    def unarchive(self, landing_id: int) -> Dict[str, Any]:
        """
        Removes a landing from archived status.

        :param landing_id: ID of the landing to unarchive
        :return: Dictionary with updated landing details
        :raises: AuthenticationError if API key is invalid
        :raises: AccessDeniedError if landing doesn't exist or permission denied
        :raises: ResourceNotFoundError if landing doesn't exist
        """
        endpoint = f"landings/{landing_id}/unarchive"
        return self.client.request("PUT", endpoint)
