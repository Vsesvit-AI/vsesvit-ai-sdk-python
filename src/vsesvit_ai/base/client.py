import requests
from typing import Optional, Dict, Any, Union
from src.vsesvit_ai.base.article import Article
from src.vsesvit_ai.base.project import Project
from src.vsesvit_ai.base.landing import Landing
from src.vsesvit_ai.base.smart_table import SmartTable
from src.vsesvit_ai.base.knowledge_base import KnowledgeBase
from src.vsesvit_ai.base.audience import Audience
from src.vsesvit_ai.base.author import Author
from src.vsesvit_ai.base.user import User
from src.vsesvit_ai.base.exceptions import NetworkError
from src.vsesvit_ai.errors.error_massages import ERROR_NETWORK
from src.vsesvit_ai.errors.error_handlers import handle_error_response
from src.vsesvit_ai.config import API_BASE_URL


class VsesvitAI:
    """The main client to work with VsesvitAI API."""

    def __init__(self, api_key: str, base_url: str = API_BASE_URL, debug: bool = False):
        """
        Initializes the VsesvitAI Client

        :param api_key: API-the authentication key you got at Vsesvit.ai
        :param base_url: Base API URL, defaults to value from .env
        :param debug: Enable debug mode to get more detailed error information
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.debug = debug
        self.article = Article(self)
        self.project = Project(self)
        self.landing = Landing(self)
        self.knowledge_base = KnowledgeBase(self)
        self.smart_table = SmartTable(self)
        self.author = Author(self)
        self.audience = Audience(self)
        self.user = User(self)

    def request(
            self,
            method: str,
            endpoint: str,
            params: Dict[str, Any] = None,
            data: Dict[str, Any] = None,
            headers: Dict[str, str] = None,
            files: Dict[str, Any] = None,
            timeout: Optional[float] = None,
            return_json: bool = True,
    ) -> Union[Dict[str, Any], bytes]:
        """
        Makes a request to the VsesvitAI API.

        :param method: HTTP Method (GET, POST, PUT, DELETE)
        :param endpoint: API endpoint (without base URL)
        :param params: Query string parameters
        :param data: Request body for POST/PUT
        :param headers: Additional HTTP headers
        :param files: Files to upload
        :param timeout: Request timeout in seconds
        :param return_json: Whether to parse response as JSON (True) or return raw content (False)
        :returns: JSON response as a dictionary or raw binary content
        :raises: VsesvitAIError or one of its subclasses on API errors
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        request_headers = {
            'X-API-KEY': self.api_key
        }

        if not headers or 'accept' not in headers:
            request_headers['accept'] = 'application/json'

        if headers:
            request_headers.update(headers)

        try:
            response = requests.request(
                method=method,
                url=url,
                params=params,
                json=data,
                headers=request_headers,
                files=files,
                timeout=timeout
            )

            if response.status_code >= 400:
                handle_error_response(
                    response=response,
                    endpoint=endpoint,
                    api_key=self.api_key,
                    debug=self.debug
                )

            if return_json:
                if response.content:
                    return response.json()
                return {}
            else:
                return response.content

        except requests.RequestException as e:
            raise NetworkError(
                message=ERROR_NETWORK.format(error=str(e)),
                original_exception=e
            )
