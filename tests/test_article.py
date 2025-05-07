import pytest
import unittest
from unittest.mock import patch

from src.vsesvit_ai.base.client import VsesvitAI


# Module-level fixtures
@pytest.fixture
def client():
    """Creates a client instance for tests."""
    api_key = "vsa_test_key123456789012345678901234"
    base_url = "https://test.vsesvit.ai/api/v1"
    return VsesvitAI(api_key=api_key, base_url=base_url)


@pytest.fixture
def article(client):
    """Creates an Article object for tests."""
    return client.article


class TestArticle:
    """Test suite for Article class."""

    @patch('src.vsesvit_ai.base.client.VsesvitAI.request')
    def test_get_list(self, mock_request, article):
        """Test getting a list of articles."""
        # Prepare mock API response with simple structure
        mock_response = {
            "data": [
                {
                    "id": 11505,
                    "name": "How to Develop a Python SDK for Vsesvit AI API",
                    "language": "en",
                    "state": "content completed",
                    "createdAt": "2025-04-28 08:36:47",
                    "updatedAt": "2025-04-28 09:27:44"
                },
                {
                    "id": 11506,
                    "name": "Top 10 Digital Marketing Trends",
                    "language": "en",
                    "state": "content completed",
                    "createdAt": "2025-04-29 10:15:30",
                    "updatedAt": "2025-04-29 11:20:15"
                }
            ],
            "meta": {
                "current_page": 1,
                "last_page": 3,
                "total": 8
            },
            "success": True
        }

        mock_request.return_value = mock_response
        params = {"page": 1, "limit": 2, "sort": "createdAt", "direction": "desc"}
        result = article.get_list(params=params)
        mock_request.assert_called_once_with("GET", "articles", params=params)

        assert result == mock_response
        assert result["success"] is True
        assert len(result["data"]) == 2
        assert result["meta"]["total"] == 8
        assert result["meta"]["current_page"] == 1
        assert result["meta"]["last_page"] == 3

    @patch('src.vsesvit_ai.base.client.VsesvitAI.request')
    def test_get_by_id(self, mock_request, article):
        """Test getting article by id"""
        mock_response = {
            "success": True,
            "data": {
                "id": 11505,
                "name": "How to Develop a Python SDK for Vsesvit AI API",
                "brief": "A detailed guide to creating an SDK for API with code examples and best practices for error handling",
                "language": "en",
                "state": "content completed",
                "createdAt": "2025-04-28 08:36:47",
                "updatedAt": "2025-04-28 09:27:44",
                "archived": False,
                "metaTitle": "Complete Guide to Python SDK Development for APIs",
                "metaDescription": "Learn how to develop a professional Python SDK for working with RESTful APIs, with focus on error handling and best practices.",
                "tags": [
                    "python",
                    "sdk",
                    "api",
                    "development",
                    "best-practices"
                ],
                "content": "<div class=\"card\">Sample content here</div>"
            }
        }

        mock_request.return_value = mock_response

        article_id = 11505
        result = article.get_by_id(article_id)
        mock_request.assert_called_once_with("GET", f"articles/{article_id}")
        assert result == mock_response
        assert result["success"] is True
        assert result["data"]["id"] == article_id
        assert result["data"]["name"] == "How to Develop a Python SDK for Vsesvit AI API"
        assert result["data"]["language"] == "en"
        assert len(result["data"]["tags"]) == 5
        assert "python" in result["data"]["tags"]
        assert "sdk" in result["data"]["tags"]

    @patch('src.vsesvit_ai.base.client.VsesvitAI.request')
    def test_create(self, mock_request, article):
        """Test creating a new article."""
        mock_response = {
            "success": True,
            "data": {
                "id": 11507,
                "name": "How to Develop a Python SDK for Vsesvit AI API",
                "brief": "A detailed guide to creating an SDK for API with code examples and best practices for error handling",
                "language": "en",
                "state": "draft",
                "createdAt": "2025-05-06 12:00:00",
                "updatedAt": "2025-05-06 12:00:00",
                "archived": False,
                "projectId": 951,
                "requestWords": 1000,
                "quality": "premium",
                "country": "US"
            }
        }

        mock_request.return_value = mock_response
        article_data = {
            "projectId": 951,
            "name": "How to Develop a Python SDK for Vsesvit AI API",
            "brief": "A detailed guide to creating an SDK for API with code examples and best practices for error handling",
            "requestWords": 1000,
            "quality": "premium",
            "country": "US",
            "language": "en",
            "useImages": True,
            "useTOC": True,
            "useBulletLists": True,
            "useQuotes": True,
            "useTables": True,
            "sections": [
                {
                    "type": "H2",
                    "title": "Introduction to SDK Development for APIs",
                    "requestWords": 300,
                    "elements": ["image", "bullet_list"]
                },
                {
                    "type": "H2",
                    "title": "Best Practices for Error Handling in SDKs",
                    "requestWords": 400,
                    "elements": ["table", "quote"]
                },
                {
                    "type": "H2",
                    "title": "Conclusions and Recommendations for SDK Development",
                    "requestWords": 300,
                    "elements": ["bullet_list"]
                }
            ]
        }

        result = article.create(article_data)
        mock_request.assert_called_once_with("POST", "articles/create", data=article_data)

        assert result == mock_response
        assert result["success"] is True
        assert result["data"]["name"] == article_data["name"]
        assert result["data"]["brief"] == article_data["brief"]
        assert result["data"]["language"] == article_data["language"]
        assert result["data"]["requestWords"] == article_data["requestWords"]
        assert result["data"]["quality"] == article_data["quality"]
        assert result["data"]["projectId"] == article_data["projectId"]

    @patch('src.vsesvit_ai.base.client.VsesvitAI.request')
    def test_download_content(self, mock_request, article):
        """Test downloading article content without saving to file."""
        mock_binary_content = b'PDF binary content'

        mock_request.return_value = mock_binary_content

        article_id = 11505
        file_format = 'pdf'

        result = article.download(article_id, file_format)
        mock_request.assert_called_once_with(
            "GET",
            f"articles/{article_id}/download/{file_format}",
            headers={'accept': 'application/octet-stream'},
            return_json=False
        )

        assert result == mock_binary_content

    @patch('src.vsesvit_ai.base.client.VsesvitAI.request')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_download_save_to_file(self, mock_file, mock_request, article):
        """Test downloading article content and saving to file."""

        mock_binary_content = b'DOCX binary content'

        mock_request.return_value = mock_binary_content

        article_id = 11505
        file_format = 'docx'
        file_path = 'my_article.docx'

        result = article.download(article_id, file_format, path=file_path)

        mock_request.assert_called_once_with(
            "GET",
            f"articles/{article_id}/download/{file_format}",
            headers={'accept': 'application/octet-stream'},
            return_json=False
        )

        mock_file.assert_called_once_with(file_path, 'wb')
        mock_file().write.assert_called_once_with(mock_binary_content)

        assert result == file_path

    @patch('src.vsesvit_ai.base.client.VsesvitAI.request')
    def test_archive(self, mock_request, article):
        """Test archiving an article."""
        mock_response = {
            "success": True,
            "data": {
                "id": 11505,
                "name": "How to Develop a Python SDK for Vsesvit AI API",
                "archived": True,
                "updatedAt": "2025-05-06 14:00:00"
            }
        }

        mock_request.return_value = mock_response
        article_id = 11505
        result = article.archive(article_id)
        mock_request.assert_called_once_with("PUT", f"articles/{article_id}/archive")

        assert result == mock_response
        assert result["success"] is True
        assert result["data"]["id"] == article_id
        assert result["data"]["archived"] is True

    @patch('src.vsesvit_ai.base.client.VsesvitAI.request')
    def test_unarchive(self, mock_request, article):
        """Test unarchiving an article."""
        mock_response = {
            "success": True,
            "data": {
                "id": 11505,
                "name": "How to Develop a Python SDK for Vsesvit AI API",
                "archived": False,
                "updatedAt": "2025-05-06 15:00:00"
            }
        }
        mock_request.return_value = mock_response
        article_id = 11505
        result = article.unarchive(article_id)

        mock_request.assert_called_once_with("PUT", f"articles/{article_id}/unarchive")

        assert result == mock_response
        assert result["success"] is True
        assert result["data"]["id"] == article_id
        assert result["data"]["archived"] is False
