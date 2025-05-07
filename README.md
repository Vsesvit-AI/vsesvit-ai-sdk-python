Вот обновленный файл README.md, включающий информацию о новых модулях и классах, при этом сохраняя существующую структуру:

```markdown
# Vsesvit AI Python SDK

![Version: 0.1.0](https://img.shields.io/badge/Version-0.1.0-blue.svg)
![Status: Beta](https://img.shields.io/badge/Status-Beta-yellow.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

## 🌐 What is Vsesvit AI?

[Vsesvit AI](https://vsesvit.ai/) is a cutting-edge platform for generating high-quality content using artificial intelligence. The service specializes in creating SEO-optimized articles, high-conversion landing pages, and automatically enhancing product tables for eCommerce.

The [Vsesvit AI](https://vsesvit.ai/) platform offers two ways to interact:
- **Web interface** at [us.vsesvit.ai](https://us.vsesvit.ai/en/register) — for manual content generation through a browser
- **Python SDK** (this library) — for automating content creation through code

This SDK serves as a bridge between your code and [Vsesvit AI](https://vsesvit.ai/) features, allowing you to integrate AI content generation into your applications, scripts, and workflows.

Detailed information about the service capabilities is available on the [official Vsesvit AI website](https://vsesvit.ai/).

## ✨ Key Features of Vsesvit AI

With Vsesvit AI SDK, you can programmatically:

- **Create SEO articles** — automatically generate search-engine optimized articles
- **Manage digital authors** — create and train unique AI writers with personal style
- **Generate landing pages** — create high-conversion landing pages
- **Enhance product tables** (SmartTables) — enrich product catalogs with unique descriptions
- **Work with knowledge bases** — use structured information for content generation
- **Configure target audiences** — adapt content for specific target groups

## 🚀 Installation

```bash
pip install vsesvit-ai
```

## 🔑 Getting an API Key

To use the SDK, you need a [Vsesvit AI](https://vsesvit.ai/) API key:

1. [Register](https://us.vsesvit.ai/en/register) on the Vsesvit AI platform
2. Log in to your account
3. Navigate to the [API Keys](https://us.vsesvit.ai/ru/account/api-keys) section
4. Click the "Create API Key" button
5. Copy the generated key (it starts with the prefix `vsa_`)

## 📚 Usage Guide

### Initializing the Client

The base client is used to send requests to the Vsesvit AI API. It establishes a connection with the server at `https://us.vsesvit.ai/api/v1` and provides authentication using your API key.

```python
from vsesvit_ai import VsesvitAI

# Create an instance of the API client
# api_key — your personal API key for authentication
# debug=True — optional, for displaying detailed error information
client = VsesvitAI(api_key="vsa_your_api_key_here", debug=False)
```

### Working with Articles

#### Getting Article List

The `get_list()` method returns a list of all articles in your account with pagination and filtering support. This is useful for viewing existing articles and managing them.

```python
# Get all articles with pagination (page 1, 10 articles per page)
articles = client.article.get_list(params={
    "page": 1,  # Page number for pagination
    "limit": 10,  # Number of articles per page
    # Additional filtering parameters:
    # "sort": "createdAt",  # Sorting (createdAt, updatedAt, name)
    # "direction": "desc",  # Sort direction (asc, desc)
    # "archived": False,  # Filter by archived articles
})

# Display the total number of articles and current page information
print(f"Total articles: {articles['meta']['total']}")
print(f"Current page: {articles['meta']['current_page']} of {articles['meta']['last_page']}")

# Process the article list
for article in articles['data']:
    print(f"ID: {article['id']} | Title: {article['name']} | Language: {article['language']}")
```

#### Getting Article Information

The `get_by_id()` method returns detailed information about an article by its ID. This method allows you to get the complete content of the article, all its parameters, and metadata.

```python
# ID of the article to retrieve
article_id = 11505

# Get detailed information about the article
article = client.article.get_by_id(article_id)

# Display basic article information
print(f"Title: {article['data']['name']}")
print(f"Created at: {article['data']['createdAt']}")
print(f"Language: {article['data']['language']}")
print(f"Status: {article['data']['state']}")

# Access article content (HTML)
content = article['data']['content']
```

#### Creating a New Article

The `create()` method allows you to programmatically create new articles. You can configure various generation parameters, including title, description, language, word count, and article structure by sections.

```python
# Data for creating an article
article_data = {
    "projectId": 951,  # Your project ID in Vsesvit AI (required field)
    "name": "How to Develop a Python SDK for Vsesvit AI API",  # Article title
    "brief": "A detailed guide to creating an SDK for API with code examples and best practices for error handling",  # Brief description
    "requestWords": 1000,  # Total word count (must match the sum of words in sections)
    "quality": "premium",  # Quality level (basic, standard, premium)
    "country": "US",  # Country code for regional content adaptation
    "language": "en",  # Article language code
    
    # Additional formatting parameters
    "useImages": True,  # Include images
    "useTOC": True,  # Create table of contents
    "useBulletLists": True,  # Use bullet lists
    "useQuotes": True,  # Include quotes
    "useTables": True,  # Include tables
    
    # Article structure by sections
    "sections": [
        {
            "type": "H2",  # Heading type (H1, H2, H3, etc.)
            "title": "Introduction to SDK Development for APIs",  # Section title
            "requestWords": 300,  # Word count for this section
            "elements": ["image", "bullet_list"]  # Formatting elements
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

# Create the article
try:
    article = client.article.create(article_data)
    print(f"Article created successfully! ID: {article['data']['id']}")
    print(f"Article URL: https://us.vsesvit.ai/en/articles/{article['data']['id']}")
except Exception as e:
    print(f"Error creating article: {e}")
```

#### Managing Articles

The Vsesvit AI SDK allows you to manage existing articles: archive them, restore them from the archive, and download them in various formats.

```python
# Article ID for management
article_id = 11505

# Archive an article
client.article.archive(article_id)
print(f"Article ID {article_id} successfully archived")

# Restore an article from the archive
client.article.unarchive(article_id)
print(f"Article ID {article_id} successfully restored from archive")

# Download an article in PDF format
# Specify article ID, format (pdf, docx) and path to save the file
file_path = client.article.download(article_id, "pdf", "my_article.pdf")
print(f"Article downloaded in PDF format and saved to file: {file_path}")

# Download an article in DOCX format
file_path = client.article.download(article_id, "docx", "my_article.docx")
print(f"Article downloaded in DOCX format and saved to file: {file_path}")
```

### Working with Projects

The SDK now supports working with projects through the `Project` class. This allows you to manage your content projects programmatically.

#### Getting Project List

The `get_list()` method returns a list of all projects in your account with pagination and filtering support.

```python
# Get all projects with pagination
projects = client.project.get_list(params={
    "page": 1,
    "limit": 10,
    "sort": "createdAt",
    "direction": "desc"
})

# Display projects information
print(f"Total projects: {projects['meta']['total']}")

# Process the project list
for project in projects['data']:
    print(f"ID: {project['id']} | Name: {project['name']}")
```

#### Getting Project Information

The `get_by_id()` method returns detailed information about a specific project.

```python
# ID of the project to retrieve
project_id = 951

# Get detailed information about the project
project = client.project.get_by_id(project_id)

# Display project information
print(f"Project name: {project['data']['name']}")
print(f"Created at: {project['data']['createdAt']}")
```

#### Creating a New Project

The `create()` method allows you to create new projects programmatically.

```python
# Data for creating a project
project_data = {
    "name": "Content Marketing Campaign",
    "description": "Project for our Q2 content marketing campaign"
}

# Create the project
try:
    project = client.project.create(project_data)
    print(f"Project created successfully! ID: {project['data']['id']}")
except Exception as e:
    print(f"Error creating project: {e}")
```

#### Managing Projects

You can archive and unarchive projects using the respective methods.

```python
# Project ID for management
project_id = 951

# Archive a project
client.project.archive(project_id)
print(f"Project ID {project_id} successfully archived")

# Restore a project from the archive
client.project.unarchive(project_id)
print(f"Project ID {project_id} successfully restored from archive")
```

## 🔄 Error Handling

The [Vsesvit AI](https://vsesvit.ai/) SDK provides an informative error handling system that allows you to accurately identify and fix any issues. All exceptions contain clear messages in natural language.

```python
from vsesvit_ai import VsesvitAI
from vsesvit_ai.errors.exceptions import (
    AuthenticationError,  # Authentication errors (invalid API key)
    AccessDeniedError,    # Resource access errors
    ResourceNotFoundError, # Non-existent resource errors
    ValidationError,      # Input data validation errors
    RateLimitError,       # Rate limit exceeded errors
    ServerError,          # Server errors
    NetworkError          # Network errors
)

try:
    # Attempt to perform an operation
    client = VsesvitAI(api_key="invalid_key")
    article = client.article.get_by_id(11505)
except AuthenticationError as e:
    print(f"Authentication error: {e}")
    print("Make sure your API key is correct and starts with 'vsa_'")
except AccessDeniedError as e:
    print(f"Access denied error: {e}")
    print("Make sure you have permission to access this resource")
except ResourceNotFoundError as e:
    print(f"Resource not found: {e}")
    print("Check the ID of the requested resource")
except ValidationError as e:
    print(f"Data validation error: {e}")
    print("Check the correctness of the parameters passed")
except NetworkError as e:
    print(f"Network error: {e}")
    print("Check your internet connection")
```

## 📋 SDK Architecture

The SDK is built with a modular architecture for extensibility and maintainability:

- **Base Client (`VsesvitAI`)**: Handles authentication and API communication
- **Resource Classes**: Provide methods for specific API resources (Article, Project)
- **Error Handling System**: Provides detailed error messages and appropriate exception types
- **Configuration System**: Centralizes SDK settings and allows for customization

## 📋 Planned Functionality

This version of the SDK supports working with articles and projects. As the [Vsesvit AI service](https://vsesvit.ai/) evolves, we will be expanding the SDK's functionality by adding:

- **Landing page operations** — generation and management of landing pages
- **SmartTables interaction** — automatic enhancement of tables
- **Digital author management** — creation and training of AI authors
- **Knowledge base operations** — management of information sources
- **Target audience configuration** — setting up reader profiles
- **And much more!**

Stay tuned for updates in our repository and on the [official Vsesvit AI website](https://vsesvit.ai/)!

## 📚 Documentation

API documentation is available at [https://us.vsesvit.ai/api/v1/doc](https://us.vsesvit.ai/api/v1/doc).

## 📄 License

This SDK is distributed under the MIT license.

## 💬 Support

If you have any questions or issues, please create an Issue in this repository.

---

Created with ❤️ by the [Vsesvit AI](https://vsesvit.ai/) team | [Register](https://us.vsesvit.ai/en/register) | [Blog](https://vsesvit.ai/blog)
```
