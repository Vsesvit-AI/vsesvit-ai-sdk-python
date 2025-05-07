import pytest
from unittest.mock import patch, Mock
import requests
from src.vsesvit_ai.base.client import VsesvitAI
from src.vsesvit_ai.base.exceptions import *
from src.vsesvit_ai.errors.error_massages import *


class TestVsesvitAIErrors:
    """Test suite for VsesvitAI client error handling."""

    def setup_method(self):
        """Set up test environment before each test."""
        self.api_key = "vsa_test_key123456789012345678901234"
        self.base_url = "https://test.vsesvit.ai/api/v1"
        self.client = VsesvitAI(api_key=self.api_key, base_url=self.base_url)

    @patch('requests.request')
    def test_network_error(self, mock_request):
        """Test handling of network errors."""
        connection_error = "Connection error"
        mock_request.side_effect = requests.RequestException(connection_error)

        with pytest.raises(NetworkError) as exc_info:
            self.client.request(method="GET", endpoint="test")

        expected_error = ERROR_NETWORK.format(error=connection_error)
        assert expected_error in str(exc_info.value)

    @patch('requests.request')
    def test_authentication_error(self, mock_request):
        """Test handling of authentication errors due to invalid API key."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.content = b'{"error": "Invalid API key"}'
        mock_response.json.return_value = {"error": "Invalid API key"}
        mock_response.text = '{"error": "Invalid API key"}'
        mock_request.return_value = mock_response

        with pytest.raises(AuthenticationError):
            self.client.request(method="GET", endpoint="test")

    @patch('requests.request')
    def test_validation_error(self, mock_request):
        """Test handling of validation errors."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.content = b'{"errors": {"param": "Invalid parameter"}}'
        mock_response.json.return_value = {"errors": {"param": "Invalid parameter"}}
        mock_response.text = '{"errors": {"param": "Invalid parameter"}}'
        mock_request.return_value = mock_response

        with pytest.raises(ValidationError):
            self.client.request(method="POST", endpoint="test", data={})

    @patch('requests.request')
    def test_rate_limit_error_with_retry(self, mock_request):
        """Test handling of rate limit errors with Retry-After header."""
        retry_seconds = "30"
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.content = b'{"error": "Too many requests"}'
        mock_response.json.return_value = {"error": "Too many requests"}
        mock_response.text = '{"error": "Too many requests"}'
        mock_response.headers = {"Retry-After": retry_seconds}
        mock_request.return_value = mock_response

        with pytest.raises(RateLimitError) as exc_info:
            self.client.request(method="GET", endpoint="test")

        assert "retry after" in str(exc_info.value).lower()
        assert retry_seconds in str(exc_info.value)

    @patch('requests.request')
    def test_rate_limit_error_without_retry(self, mock_request):
        """Test handling of rate limit errors without Retry-After header."""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.content = b'{"error": "Too many requests"}'
        mock_response.json.return_value = {"error": "Too many requests"}
        mock_response.text = '{"error": "Too many requests"}'
        mock_response.headers = {}
        mock_request.return_value = mock_response

        with pytest.raises(RateLimitError):
            self.client.request(method="GET", endpoint="test")

    @patch('requests.request')
    def test_server_error(self, mock_request):
        """Test handling of server errors."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.content = b'{"error": "Internal server error"}'
        mock_response.json.return_value = {"error": "Internal server error"}
        mock_response.text = '{"error": "Internal server error"}'
        mock_request.return_value = mock_response

        with pytest.raises(ServerError):
            self.client.request(method="GET", endpoint="test")