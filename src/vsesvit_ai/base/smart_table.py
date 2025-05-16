from typing import Dict, Any, Union, Optional, BinaryIO


class SmartTable:
    def __init__(self, client):
        """
        Initialize the SmartTable resource

        :param client: VsesvitAI client instance
        """
        self.client = client

    def get_list(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Get a list of smart tables with pagination and filtering options.

        :param params: Query parameters for filtering and pagination
        :return: Dictionary with smart tables list and pagination info
        :raises: AuthenticationError if API key is invalid
        :raises: AccessDeniedError if permission denied
        :raises: ValidationError if query parameters are invalid
        """
        return self.client.request("GET", "smart-tables", params=params)

    def get_by_id(self, table_id: int) -> Dict[str, Any]:
        """
        Returns detailed information about a specific smart table.

        :param table_id: ID of the smart table to retrieve
        :return: Dictionary with smart table details
        :raises: AuthenticationError if API key is invalid
        :raises: AccessDeniedError if smart table doesn't exist or permission denied
        :raises: ResourceNotFoundError if smart table doesn't exist
        """
        return self.client.request("GET", f"smart-tables/{table_id}")

    def upload(self, file: Union[str, BinaryIO], file_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Upload a file to be processed by a smart table.

        You can pass either a file path or a file object.
        If a file object is provided, you must specify the file_name parameter.

        :param file: Path to the file or a file-like object
        :param file_name: Name of the file (required if file is a file object)
        :return: Dictionary with uploaded file details, including ID for creating a table
        :raises: AuthenticationError if API key is invalid
        :raises: ValidationError if file format is invalid
        :raises: AccessDeniedError if permission denied
        """
        if isinstance(file, str):
            # If file is a path, open the file and read its content
            with open(file, 'rb') as f:
                file_data = f.read()
                file_name = file_name or file.split('/')[-1]
        else:
            # If file is a file-like object, read its content
            file_data = file.read()
            if not file_name:
                raise ValueError("file_name is required when file is a file object")

        files = {'file': (file_name, file_data)}
        return self.client.request("POST", "smart-tables/upload-file", files=files)

    def create(self, project_id: int, name: str, brief: str, input_asset_id: int,
               additional_params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Create a new smart table based on uploaded file.

        Typically you would first upload a file using the upload method,
        then use the returned file ID to create a smart table.

        :param project_id: ID of the project to create the smart table in
        :param name: Smart table title
        :param brief: Detailed instructions for smart table generation
        :param input_asset_id: ID of the input asset (XLSX file) from upload method
        :param additional_params: Optional parameters including:
            - quality (str): Quality level for content generation (premium/standard)
            - limitRows (int): Number of rows to process (0 for all)
            - offsetRows (int): Number of rows to skip before processing
            - columns (list): Column definitions for the smart table
        :return: Dictionary with created smart table details
        :raises: AuthenticationError if API key is invalid
        :raises: ValidationError if required parameters are missing
        :raises: AccessDeniedError if permission denied
        """
        data = {
            'projectId': project_id,
            'name': name,
            'brief': brief,
            'inputAssetId': input_asset_id
        }

        if additional_params:
            data.update(additional_params)

        return self.client.request("POST", "smart-tables/create", data=data)

    def download(self, table_id: int, format: str = "xlsx", path: Optional[str] = None) -> Union[bytes, str]:
        """
        Download a smart table in the specified format.

        :param table_id: ID of the smart table to download
        :param format: Format to download (default: "xlsx")
        :param path: Optional file path to save the downloaded file
        :return: File content as bytes or path string if path is provided
        :raises: AuthenticationError if API key is invalid
        :raises: AccessDeniedError if smart table doesn't exist or permission denied
        :raises: ResourceNotFoundError if smart table doesn't exist
        :raises: ValidationError if format is invalid
        """
        endpoint = f"smart-tables/{table_id}/download"
        params = {"format": format} if format else None
        headers = {'accept': 'application/octet-stream'}
        content = self.client.request("GET", endpoint, params=params, headers=headers, return_json=False)

        if path:
            with open(path, 'wb') as file:
                file.write(content)
            return path
        else:
            return content

    def archive(self, table_id: int) -> Dict[str, Any]:
        """
        Archive a smart table.

        :param table_id: ID of the smart table to archive
        :return: Dictionary with updated smart table details
        :raises: AuthenticationError if API key is invalid
        :raises: AccessDeniedError if smart table doesn't exist or permission denied
        :raises: ResourceNotFoundError if smart table doesn't exist
        """
        endpoint = f"smart-tables/{table_id}/archive"
        return self.client.request("PUT", endpoint)

    def unarchive(self, table_id: int) -> Dict[str, Any]:
        """
        Unarchive a smart table.

        :param table_id: ID of the smart table to unarchive
        :return: Dictionary with updated smart table details
        :raises: AuthenticationError if API key is invalid
        :raises: AccessDeniedError if smart table doesn't exist or permission denied
        :raises: ResourceNotFoundError if smart table doesn't exist
        """
        endpoint = f"smart-tables/{table_id}/unarchive"
        return self.client.request("PUT", endpoint)