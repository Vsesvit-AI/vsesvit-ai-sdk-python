import pytest
from unittest.mock import patch, Mock
from src.vsesvit_ai.base.client import VsesvitAI
from src.vsesvit_ai.base.exceptions import *
from src.vsesvit_ai.errors.error_massages import *


class TestArticleErrors:
    """Test suite for Article resource error handling."""

    def setup_method(self):
        """Set up test environment before each test."""
        self.api_key = "vsa_test_key123456789012345678901234"
        self.base_url = "https://test.vsesvit.ai/api/v1"
        self.client = VsesvitAI(api_key=self.api_key, base_url=self.base_url)
        self.article = self.client.article

    @patch('requests.request')
    def test_get_list_authentication_error(self, mock_request):
        """Test handling of authentication errors when getting article list."""
        # Setup mock response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.content = b'{"error": "Invalid API key"}'
        mock_response.json.return_value = {"error": "Invalid API key"}
        mock_response.text = '{"error": "Invalid API key"}'

        mock_response.headers = {}
        mock_request.return_value = mock_response

        original_api_key = self.client.api_key
        self.client.api_key = "invalid_key"

        try:
            with pytest.raises(AuthenticationError) as exc_info:
                self.article.get_list()

            assert ERROR_INVALID_API_KEY in str(exc_info.value)
        finally:
            self.client.api_key = original_api_key

    @patch('requests.request')
    def test_get_list_validation_error(self, mock_request):
        """Test handling of validation errors when getting article list with invalid params."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.content = b'{"errors": {"page": "Must be a positive integer"}}'
        mock_response.json.return_value = {"errors": {"page": "Must be a positive integer"}}
        mock_response.text = '{"errors": {"page": "Must be a positive integer"}}'
        mock_request.return_value = mock_response

        with pytest.raises(ValidationError) as exc_info:
            self.article.get_list(params={"page": -1})

        assert "page" in str(exc_info.value)
        assert "Must be a positive integer" in str(exc_info.value)

    @patch('requests.request')
    @patch('src.vsesvit_ai.errors.error_handlers.parse_resource_info')
    def test_get_by_id_resource_not_found(self, mock_parse_resource, mock_request):
        """Test handling of resource not found errors when getting non-existent article."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.content = b'{"error": "Article not found"}'
        mock_response.json.return_value = {"error": "Article not found"}
        mock_response.text = '{"error": "Article not found"}'
        mock_request.return_value = mock_response

        article_id = 99999
        mock_parse_resource.return_value = ("article", str(article_id))

        with pytest.raises(ResourceNotFoundError) as exc_info:
            self.article.get_by_id(article_id)

        assert "article" in str(exc_info.value).lower()

    @patch('requests.request')
    @patch('src.vsesvit_ai.errors.error_handlers.parse_resource_info')
    def test_get_by_id_access_denied(self, mock_parse_resource, mock_request):
        """Test handling of access denied errors when getting article without permission."""
        mock_response = Mock()
        mock_response.status_code = 403  # Changed from 401 to 403 for access denied
        mock_response.content = b'{"error": "Access denied"}'
        mock_response.json.return_value = {"error": "Access denied"}
        mock_response.text = '{"error": "Access denied"}'
        mock_request.return_value = mock_response

        article_id = 11505
        mock_parse_resource.return_value = ("article", str(article_id))

        with pytest.raises(AccessDeniedError) as exc_info:
            self.article.get_by_id(article_id)

        assert "article" in str(exc_info.value).lower()

    @patch('requests.request')
    def test_create_validation_error(self, mock_request):
        """Test handling of validation errors when creating article with invalid data."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.content = b'{"errors": {"name": "Name is required", "language": "Invalid language code"}}'
        mock_response.json.return_value = {"errors": {"name": "Name is required", "language": "Invalid language code"}}
        mock_response.text = '{"errors": {"name": "Name is required", "language": "Invalid language code"}}'
        mock_request.return_value = mock_response

        with pytest.raises(ValidationError) as exc_info:
            self.article.create(data={"projectId": 951})

        error_message = str(exc_info.value)
        assert "name" in error_message
        assert "language" in error_message
        assert "Name is required" in error_message
        assert "Invalid language code" in error_message

    @patch('requests.request')
    def test_create_server_error(self, mock_request):
        """Test handling of server errors when creating article."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.content = b'{"error": "Internal server error"}'
        mock_response.json.return_value = {"error": "Internal server error"}
        mock_response.text = '{"error": "Internal server error"}'
        mock_request.return_value = mock_response

        article_data = {
            "projectId": 951,
            "name": "Test Article",
            "language": "en"
        }

        with pytest.raises(ServerError):
            self.article.create(data=article_data)

    @patch('requests.request')
    def test_download_invalid_format(self, mock_request):
        """Test handling of validation errors when downloading article with invalid format."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.content = b'{"errors": {"format": "Invalid format specified. Available formats: pdf, docx"}}'
        mock_response.json.return_value = {
            "errors": {"format": "Invalid format specified. Available formats: pdf, docx"}}
        mock_response.text = '{"errors": {"format": "Invalid format specified. Available formats: pdf, docx"}}'
        mock_request.return_value = mock_response

        article_id = 11505
        invalid_format = "txt"

        with pytest.raises(ValidationError) as exc_info:
            self.article.download(article_id, invalid_format)

        assert "format" in str(exc_info.value)
        assert "Invalid format" in str(exc_info.value)

    @patch('requests.request')
    @patch('src.vsesvit_ai.errors.error_handlers.parse_resource_info')
    def test_download_resource_not_found(self, mock_parse_resource, mock_request):
        """Test handling of resource not found errors when downloading non-existent article."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.content = b'{"error": "Article not found"}'
        mock_response.json.return_value = {"error": "Article not found"}
        mock_response.text = '{"error": "Article not found"}'
        mock_request.return_value = mock_response

        article_id = 99999
        mock_parse_resource.return_value = ("article", str(article_id))

        with pytest.raises(ResourceNotFoundError) as exc_info:
            self.article.download(article_id, "pdf")

        assert "article" in str(exc_info.value).lower()

    @patch('requests.request')
    @patch('src.vsesvit_ai.errors.error_handlers.parse_resource_info')
    def test_archive_resource_not_found(self, mock_parse_resource, mock_request):
        """Test handling of resource not found errors when archiving non-existent article."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.content = b'{"error": "Article not found"}'
        mock_response.json.return_value = {"error": "Article not found"}
        mock_response.text = '{"error": "Article not found"}'
        mock_request.return_value = mock_response

        article_id = 99999
        mock_parse_resource.return_value = ("article", str(article_id))

        with pytest.raises(ResourceNotFoundError) as exc_info:
            self.article.archive(article_id)

        assert "article" in str(exc_info.value).lower()

    @patch('requests.request')
    @patch('src.vsesvit_ai.errors.error_handlers.parse_resource_info')
    def test_get_by_id_access_denied(self, mock_parse_resource, mock_request):
        """Test handling of access denied errors when getting article without permission."""
        mock_response = Mock()
        mock_response.status_code = 403  # Changed from 401 to 403 for access denied
        mock_response.content = b'{"error": "Access denied to this article"}'
        mock_response.json.return_value = {"error": "Access denied to this article"}
        mock_response.text = '{"error": "Access denied to this article"}'
        mock_request.return_value = mock_response

        article_id = 11505
        mock_parse_resource.return_value = ("article", str(article_id))

        with pytest.raises(AccessDeniedError) as exc_info:
            self.article.get_by_id(article_id)

        assert "access denied" in str(exc_info.value).lower()  # Проверяем по основному тексту ошибки

    @patch('requests.request')
    def test_rate_limit_exceeded(self, mock_request):
        """Test handling of rate limit errors when making too many requests to article API."""
        retry_seconds = "60"
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.content = b'{"error": "API rate limit exceeded"}'
        mock_response.json.return_value = {"error": "API rate limit exceeded"}
        mock_response.text = '{"error": "API rate limit exceeded"}'
        mock_response.headers = {"Retry-After": retry_seconds}
        mock_request.return_value = mock_response

        with pytest.raises(RateLimitError) as exc_info:
            self.article.get_list(params={"page": 1, "limit": 100})  # Request with large limit

        assert "retry after" in str(exc_info.value).lower()
        assert retry_seconds in str(exc_info.value)