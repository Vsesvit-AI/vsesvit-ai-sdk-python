from unittest.mock import patch, Mock
from src.vsesvit_ai.base.client import VsesvitAI


class TestVsesvitAI:
    """Test suite for VsesvitAI client."""

    def setup_method(self):
        """Set up test environment before each test."""
        self.api_key = "vsa_test_key123456789012345678901234"
        self.base_url = "https://test.vsesvit.ai/api/v1"
        self.client = VsesvitAI(api_key=self.api_key, base_url=self.base_url)

    def test_init(self):
        """Test client initialization."""

        assert self.client.api_key == self.api_key
        assert self.client.base_url == self.base_url
        assert self.client.debug is False

        assert self.client.article is not None

    def test_init_with_trailing_slash(self):
        """Test that trailing slash in base_url is removed."""
        client = VsesvitAI(api_key=self.api_key, base_url=f"{self.base_url}/")
        assert client.base_url == self.base_url

    def test_init_with_debug(self):
        """Test debug mode initialization."""
        debug_client = VsesvitAI(api_key=self.api_key, base_url=self.base_url, debug=True)
        assert debug_client.debug is True

    @patch('requests.request')
    def test_request_success(self, mock_request):
        """Test successful API request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'{"success": true, "data": {"id": 123}}'
        mock_response.json.return_value = {"success": True, "data": {"id": 123}}
        mock_request.return_value = mock_response

        result = self.client.request(
            method="GET",
            endpoint="test/endpoint",
            params={"param1": "value1"},
            data={"data1": "value1"}
        )

        mock_request.assert_called_once_with(
            method="GET",
            url=f"{self.base_url}/test/endpoint",
            params={"param1": "value1"},
            json={"data1": "value1"},
            headers={"X-API-KEY": self.api_key, "accept": "application/json"},
            files=None,
            timeout=None
        )

        assert result == {"success": True, "data": {"id": 123}}

    @patch('requests.request')
    def test_request_custom_headers(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'{}'
        mock_response.json.return_value = {}
        mock_request.return_value = mock_response

        self.client.request(
            method="GET",
            endpoint="test",
            headers={"Custom-Header": "value", "accept": "text/plain"}
        )

        expected_headers = {
            "X-API-KEY": self.api_key,
            "Custom-Header": "value",
            "accept": "text/plain"
        }

        called_kwargs = mock_request.call_args[1]
        assert called_kwargs["headers"] == expected_headers

    @patch('requests.request')
    def test_request_binary_response(self, mock_request):
        """Test request with binary response."""
        binary_data = b'binary data'

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = binary_data
        mock_request.return_value = mock_response

        result = self.client.request(
            method="GET",
            endpoint="download",
            return_json=False
        )

        assert result == binary_data
