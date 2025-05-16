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

    def create(self, project_id: int, name: str, brief: str,
               additional_params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Create a new landing with flexible configuration options.

        :param project_id: ID of the project to create the landing in
        :param name: Landing title
        :param brief: Detailed description of what the landing should cover
        :param additional_params: Optional parameters including:
            - requestSections (int): Requested number of sections for the landing (default: 10)
            - quality (str): Quality level for content generation (premium/standard)
            - country (str): ISO country code for region-specific content
            - language (str): ISO language code for content language (default: 'en')
            - imageModel (str): Model to use for image generation
            - publishUrl (str): URL where the landing page will be published
            - formHandlerUrl (str): Form handler URL for any forms on the landing page
            - privacyPolicy (str): Privacy policy text or link
            - termsAndConditions (str): Terms and conditions text or link
            - useChartJs (bool): Whether to use Chart.js
            - useSwiper (bool): Whether to use Swiper
            - useAOS (bool): Whether to use AOS (Animate on Scroll)
            - useTypedJs (bool): Whether to use Typed.js
            - useVanilaTiltJs (bool): Whether to use Vanilla Tilt.js
            - useScrollReveal (bool): Whether to use ScrollReveal
            - useCountUpJs (bool): Whether to use CountUp.js
            - useRellax (bool): Whether to use Rellax
            - useGlowCookies (bool): Whether to use GlowCookies
            - templateId (int): ID of the template to use
            - audienceId (int): ID of the target audience
            - knowledgeIds (list): IDs of knowledge bases to use
            - keywords (list): Keywords to include in landing (list of dicts with 'value' and 'quantity')
            - rules (list): Writing style rules to follow (list of dicts with 'rule')
            - externalLinks (list): External links to include (list of dicts with 'url')
            - contentSources (list): Source URLs for content research (list of dicts with 'url')
            - sections (list): Landing sections (null to let AI generate sections automatically)
        :return: Dictionary with created landing details
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