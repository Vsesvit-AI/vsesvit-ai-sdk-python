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

    def create(self, project_id: int, name: str,
               additional_params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Create a new audience for a specific project.

        :param project_id: ID of the project to create the audience in
        :param name: Audience name
        :param additional_params: Optional parameters including:
            - ageGroup (str): Age group of the audience
            - gender (str): Gender of the audience
            - occupation (str): Occupation of the audience
            - educationLevel (str): Education level of the audience
            - incomeBracket (str): Income bracket of the audience
            - relationshipStatus (str): Relationship status of the audience
            - lifeStage (str): Life stage of the audience
            - goals (str): Goals of the audience
            - coreValues (str): Core values of the audience
            - hobbies (str): Hobbies of the audience
            - behavioralTraits (str): Behavioral traits of the audience
            - visualPreferences (str): Visual preferences of the audience
            - communicationStyle (str): Communication style of the audience
            - interests (str): Interests of the audience
            - painPoints (str): Pain points of the audience
            - triggers (str): Triggers that motivate the audience
            - languageVarieties (str): Language varieties or preferences
        :return: Dictionary with created audience details
        :raises: AuthenticationError if API key is invalid
        :raises: ValidationError if required parameters are missing
        :raises: AccessDeniedError if permission denied
        :raises: ResourceNotFoundError if project doesn't exist
        """
        data = {
            'projectId': project_id,
            'name': name
        }

        if additional_params:
            data.update(additional_params)

        return self.client.request("POST", "audiences/create", data=data)

    def archive(self, audience_id: int) -> Dict[str, Any]:
        """
        Archives an audience.

        :param audience_id: ID of the audience to archive
        :return: Dictionary with updated audience details
        :raises: AuthenticationError if API key is invalid
        :raises: AccessDeniedError if audience doesn't exist or permission denied
        :raises: ResourceNotFoundError if audience doesn't exist
        """
        endpoint = f"audiences/{audience_id}/archive"
        return self.client.request("PUT", endpoint)

    def unarchive(self, audience_id: int) -> Dict[str, Any]:
        """
        Removes an audience from archived status.

        :param audience_id: ID of the audience to unarchive
        :return: Dictionary with updated audience details
        :raises: AuthenticationError if API key is invalid
        :raises: AccessDeniedError if audience doesn't exist or permission denied
        :raises: ResourceNotFoundError if audience doesn't exist
        """
        endpoint = f"audiences/{audience_id}/unarchive"
        return self.client.request("PUT", endpoint)