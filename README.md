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

### Via pip (recommended)

```bash
pip install vsesvit-ai
```

### From source

```bash
git clone https://github.com/vsesvitai/vsesvit-ai-python.git
cd vsesvit-ai-python
pip install -e .
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

The `create()` method allows you to programmatically create new articles. The method now has mandatory parameters separated from optional ones for better clarity and IDE support.

```python
# Create an article with required parameters
article = client.article.create(
    project_id=951,  # Your project ID in Vsesvit AI (required)
    name="How to Develop a Python SDK for Vsesvit AI API",  # Article title (required)
    brief="A detailed guide to creating an SDK for API with code examples and best practices for error handling",  # Brief description (required)
    additional_params={
        "requestWords": 1000,  # Total word count (default: 3000)
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
)

print(f"Article created successfully! ID: {article['data']['id']}")
print(f"Article URL: https://us.vsesvit.ai/en/articles/{article['data']['id']}")
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

The `create()` method allows you to create new projects programmatically with required parameters separated.

```python
# Create a project with required parameters
project = client.project.create(
    name="Content Marketing Campaign",  # Project name (required)
    description="Project for our Q2 content marketing campaign"  # Detailed description (required)
)

print(f"Project created successfully! ID: {project['data']['id']}")
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

### Working with Landing Pages

The SDK provides functionality for working with landing pages through the `Landing` class.

#### Getting Landing Page List

The `get_list()` method returns a list of all landing pages in your account with pagination and filtering options.

```python
# Get all landing pages with pagination
landings = client.landing.get_list(params={
    "page": 1,
    "limit": 10,
    "sort": "createdAt",
    "direction": "desc"
})

# Display landing pages information
print(f"Total landing pages: {landings['meta']['total']}")

# Process the landing page list
for landing in landings['data']:
    print(f"ID: {landing['id']} | Name: {landing['name']}")
```

#### Getting Landing Page Information

The `get_by_id()` method returns detailed information about a specific landing page.

```python
# ID of the landing page to retrieve
landing_id = 123

# Get detailed information about the landing page
landing = client.landing.get_by_id(landing_id)

# Display landing page information
print(f"Landing page name: {landing['data']['name']}")
print(f"Created at: {landing['data']['createdAt']}")
print(f"Status: {landing['data']['state']}")
```

#### Creating a New Landing Page

The `create()` method allows you to create new landing pages with required parameters separated for better clarity.

```python
# Create a landing page with required parameters
landing = client.landing.create(
    project_id=951,  # Your project ID in Vsesvit AI (required)
    name="Product Launch Landing Page",  # Landing page title (required)
    brief="A landing page for our new product launch with emphasis on benefits and call-to-action",  # Brief description (required)
    additional_params={
        "requestSections": 5,  # Requested number of sections (default: 10)
        "quality": "premium",  # Quality level (basic, standard, premium)
        "country": "US",  # Country code for regional content adaptation
        "language": "en",  # Landing page language code
        "imageModel": "dalle3",  # Model for image generation
        "publishUrl": "https://example.com/product-launch",  # URL where the landing will be published
        "formHandlerUrl": "https://example.com/form-handler",  # Form handler URL
        "privacyPolicy": "https://example.com/privacy",  # Privacy policy link
        "termsAndConditions": "https://example.com/terms",  # Terms and conditions link
        
        # Optional JavaScript libraries to include
        "useChartJs": False,
        "useSwiper": True,
        "useAOS": True,
        "useTypedJs": False,
        "useVanilaTiltJs": False,
        "useScrollReveal": True,
        "useCountUpJs": False,
        "useRellax": False,
        "useGlowCookies": True,
        
        # Optional template and audience configuration
        "templateId": 1,  # ID of the template to use
        "audienceId": 2,  # ID of the target audience
        "knowledgeIds": [3, 4],  # IDs of knowledge bases to use
        
        # Optional content configuration
        "keywords": [{"value": "product launch", "quantity": 3}],  # Keywords to include
        "rules": [{"rule": "Focus on benefits"}],  # Writing style rules
        "externalLinks": [{"url": "https://example.com/product-details"}],  # External links
        "contentSources": [{"url": "https://example.com/product-blog"}],  # Source URLs
        
        # Optional section configuration
        "sections": [
            {
                "type": "header",
                "title": "Revolutionary New Product"
            },
            {
                "type": "benefits",
                "title": "Key Benefits"
            }
        ]
    }
)

print(f"Landing page created successfully! ID: {landing['data']['id']}")
print(f"Landing page URL: https://us.vsesvit.ai/en/landings/{landing['data']['id']}")
```

#### Downloading a Landing Page

The `download()` method allows you to download a landing page as a ZIP file.

```python
# Landing page ID for download
landing_id = 123

# Download a landing page in ZIP format
# Specify landing ID and path to save the file
file_path = client.landing.download(landing_id, "my_landing.zip")
print(f"Landing page downloaded as ZIP and saved to file: {file_path}")
```

#### Managing Landing Pages

You can archive and unarchive landing pages using the respective methods.

```python
# Landing page ID for management
landing_id = 123

# Archive a landing page
client.landing.archive(landing_id)
print(f"Landing page ID {landing_id} successfully archived")

# Restore a landing page from the archive
client.landing.unarchive(landing_id)
print(f"Landing page ID {landing_id} successfully restored from archive")
```

### Working with Smart Tables

The SDK offers functionality for enhancing product tables through the `SmartTable` class.

#### Getting Smart Table List

The `get_list()` method returns a list of all smart tables in your account with pagination and filtering options.

```python
# Get all smart tables with pagination
smart_tables = client.smart_table.get_list(params={
    "page": 1,
    "limit": 10,
    "sort": "createdAt",
    "direction": "desc"
})

# Display smart tables information
print(f"Total smart tables: {smart_tables['meta']['total']}")

# Process the smart table list
for table in smart_tables['data']:
    print(f"ID: {table['id']} | Name: {table['name']}")
```

#### Getting Smart Table Information

The `get_by_id()` method returns detailed information about a specific smart table.

```python
# ID of the smart table to retrieve
table_id = 456

# Get detailed information about the smart table
table = client.smart_table.get_by_id(table_id)

# Display smart table information
print(f"Smart table name: {table['data']['name']}")
print(f"Created at: {table['data']['createdAt']}")
print(f"Status: {table['data']['state']}")
```

#### Uploading a File for Smart Table Processing

Before creating a smart table, you need to upload an XLSX file that will be enhanced.

```python
# Path to the XLSX file on your local machine
file_path = "products.xlsx"

# Upload the file
try:
    upload_result = client.smart_table.upload(file_path)
    input_asset_id = upload_result["data"]["id"]
    print(f"File uploaded successfully! Asset ID: {input_asset_id}")
    
    # This input_asset_id will be used when creating the smart table
except Exception as e:
    print(f"Error uploading file: {e}")
```

#### Creating a New Smart Table

After uploading a file, you can create a smart table using the `create()` method with required parameters separated.

```python
# Create a smart table with required parameters, using the input_asset_id from upload
smart_table = client.smart_table.create(
    project_id=951,  # Your project ID in Vsesvit AI (required)
    name="Product Catalog Enhancement",  # Smart table title (required)
    brief="Generate compelling product descriptions based on the technical specifications",  # Brief instructions (required)
    input_asset_id=input_asset_id,  # ID of the uploaded XLSX file (required)
    additional_params={
        "quality": "premium",  # Quality level (basic, standard, premium)
        "limitRows": 0,  # Number of rows to process (0 for all)
        "offsetRows": 0,  # Number of rows to skip before processing
        
        # Column definitions for processing
        "columns": [
            {
                "name": "Product Name",  # Column name from the original file
                "action": "keep"  # Keep the original data
            },
            {
                "name": "Technical Specs",  # Column name from the original file
                "action": "source"  # Use as a source for enhancement
            },
            {
                "name": "Description",  # New column name
                "action": "generate",  # Generate content for this column
                "prompt": "Create a compelling product description",  # Instructions
                "maxWords": 100  # Maximum word count for generated content
            }
        ]
    }
)

print(f"Smart table created successfully! ID: {smart_table['data']['id']}")
print(f"Smart table URL: https://us.vsesvit.ai/en/smart-tables/{smart_table['data']['id']}")
```

#### Downloading a Smart Table

The `download()` method allows you to download the enhanced smart table as an XLSX file.

```python
# Smart table ID for download
table_id = 456

# Download a smart table in XLSX format
# Specify table ID and path to save the file
file_path = client.smart_table.download(table_id, "enhanced_products.xlsx")
print(f"Smart table downloaded as XLSX and saved to file: {file_path}")
```

#### Managing Smart Tables

You can archive and unarchive smart tables using the respective methods.

```python
# Smart table ID for management
table_id = 456

# Archive a smart table
client.smart_table.archive(table_id)
print(f"Smart table ID {table_id} successfully archived")

# Restore a smart table from the archive
client.smart_table.unarchive(table_id)
print(f"Smart table ID {table_id} successfully restored from archive")
```

### Working with Knowledge Bases

The SDK provides access to knowledge bases through the `KnowledgeBase` class.

#### Getting Knowledge Base List

The `get_list()` method returns a list of all knowledge bases in your account with pagination and filtering options.

```python
# Get all knowledge bases with pagination
knowledge_bases = client.knowledge_base.get_list(params={
    "page": 1,
    "limit": 10
})

# Display knowledge bases information
print(f"Total knowledge bases: {knowledge_bases['meta']['total']}")

# Process the knowledge base list
for kb in knowledge_bases['data']:
    print(f"ID: {kb['id']} | Name: {kb['name']}")
```

#### Getting Knowledge Base Information

The `get_by_id()` method returns detailed information about a specific knowledge base.

```python
# ID of the knowledge base to retrieve
kb_id = 789

# Get detailed information about the knowledge base
kb = client.knowledge_base.get_by_id(kb_id)

# Display knowledge base information
print(f"Knowledge base name: {kb['data']['name']}")
print(f"Created at: {kb['data']['createdAt']}")
```

#### Creating a New Knowledge Base

The `create()` method allows you to create new knowledge bases with required parameters separated.

```python
# Create a knowledge base with required parameters
kb = client.knowledge_base.create(
    project_id=951,  # Your project ID in Vsesvit AI (required)
    name="Company Documentation",  # Knowledge base name (required)
    description="Comprehensive documentation for our company products and services",  # Description (required)
    additional_params={
        "language": "en",  # Language of the knowledge base (ISO 639-1 code)
        "sources": [
            {"url": "https://docs.company.com/products"},  # Web sources
            {"query": "company product documentation"}  # Search-based sources
        ]
    }
)

print(f"Knowledge base created successfully! ID: {kb['data']['id']}")
```

#### Managing Knowledge Bases

You can archive and unarchive knowledge bases using the respective methods.

```python
# Knowledge base ID for management
kb_id = 789

# Archive a knowledge base
client.knowledge_base.archive(kb_id)
print(f"Knowledge base ID {kb_id} successfully archived")

# Restore a knowledge base from the archive
client.knowledge_base.unarchive(kb_id)
print(f"Knowledge base ID {kb_id} successfully restored from archive")
```

### Working with Authors

The SDK allows you to interact with digital authors through the `Author` class.

#### Getting Author List

The `get_list()` method returns a list of all authors in your account with pagination and filtering options.

```python
# Get all authors with pagination
authors = client.author.get_list(params={
    "page": 1,
    "limit": 10
})

# Display authors information
print(f"Total authors: {authors['meta']['total']}")

# Process the author list
for author in authors['data']:
    print(f"ID: {author['id']} | Name: {author['name']}")
```

#### Getting Author Information

The `get_by_id()` method returns detailed information about a specific author.

```python
# ID of the author to retrieve
author_id = 321

# Get detailed information about the author
author = client.author.get_by_id(author_id)

# Display author information
print(f"Author name: {author['data']['name']}")
print(f"Created at: {author['data']['createdAt']}")
print(f"Biography: {author['data']['biography']}")
```

#### Creating a New Author

The `create()` method allows you to create new authors with required parameters separated.

```python
# Create an author with required parameters
author = client.author.create(
    project_id=951,  # Your project ID in Vsesvit AI (required)
    name="John Smith",  # Author name (required)
    biography="John Smith is a senior software engineer with over 15 years of experience in web development.",  # Biography (required)
    additional_params={
        "ppm": {  # Author persona parameters
            "writing_style": "technical",
            "tone": "professional",
            "expertise": "web development"
        },
        "sources": [  # Training sources for the author's writing style
            {"url": "https://example.com/author-articles"},
            {"url": "https://medium.com/@johnsmith"}
        ]
    }
)

print(f"Author created successfully! ID: {author['data']['id']}")
```

#### Managing Authors

You can archive and unarchive authors using the respective methods.

```python
# Author ID for management
author_id = 321

# Archive an author
client.author.archive(author_id)
print(f"Author ID {author_id} successfully archived")

# Restore an author from the archive
client.author.unarchive(author_id)
print(f"Author ID {author_id} successfully restored from archive")
```

### Working with Audiences

The SDK provides functionality for managing target audiences through the `Audience` class.

#### Getting Audience List

The `get_list()` method returns a list of all audiences in your account with pagination and filtering options.

```python
# Get all audiences with pagination
audiences = client.audience.get_list(params={
    "page": 1,
    "limit": 10
})

# Display audiences information
print(f"Total audiences: {audiences['meta']['total']}")

# Process the audience list
for audience in audiences['data']:
    print(f"ID: {audience['id']} | Name: {audience['name']}")
```

#### Getting Audience Information

The `get_by_id()` method returns detailed information about a specific audience.

```python
# ID of the audience to retrieve
audience_id = 654

# Get detailed information about the audience
audience = client.audience.get_by_id(audience_id)

# Display audience information
print(f"Audience name: {audience['data']['name']}")
print(f"Created at: {audience['data']['createdAt']}")
```

#### Creating a New Audience

The `create()` method allows you to create new audiences with required parameters separated.

```python
# Create an audience with required parameters
audience = client.audience.create(
    project_id=951,  # Your project ID in Vsesvit AI (required)
    name="Young Professionals",  # Audience name (required)
    additional_params={
        "ageGroup": "25-35",
        "gender": "All genders",
        "occupation": "IT professionals, software developers, project managers",
        "educationLevel": "Bachelor's degree or higher",
        "incomeBracket": "$50,000 - $100,000 annually",
        "interests": "Technology, career development, productivity",
        "painPoints": "Time management, work-life balance, career growth"
    }
)

print(f"Audience created successfully! ID: {audience['data']['id']}")
```

#### Managing Audiences

You can archive and unarchive audiences using the respective methods.

```python
# Audience ID for management
audience_id = 654

# Archive an audience
client.audience.archive(audience_id)
print(f"Audience ID {audience_id} successfully archived")

# Restore an audience from the archive
client.audience.unarchive(audience_id)
print(f"Audience ID {audience_id} successfully restored from archive")
```

### Working with User Information

The SDK provides access to user information through the `User` class.

#### Getting Current User Information

The `get_me()` method returns information about the current authenticated user.

```python
# Get information about the current user
user = client.user.get_me()

# Display user information
print(f"User ID: {user['data']['id']}")
print(f"Email: {user['data']['email']}")
print(f"Full Name: {user['data']['fullName']}")
print(f"Company: {user['data']['company']}")
print(f"Balance: {user['data']['balance']}")
```

#### Getting Referrals Information

The `get_referrals()` method returns a list of users who signed up using the current user's referral code.

```python
# Get referrals with pagination and search options
referrals = client.user.get_referrals(params={
    "offset": 0,  # Number of items to skip
    "limit": 10,  # Number of items to return
    "search": ""  # Search string to filter referrals by name (optional)
})

# Display referrals information
if 'data' in referrals and len(referrals['data']) > 0:
    print(f"Total referrals: {len(referrals['data'])}")
    
    # Process the referrals list
    for referral in referrals['data']:
        print(f"ID: {referral['id']} | Name: {referral['name']} | Joined: {referral['createdAt']}")
else:
    print("No referrals found")
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
- **Resource Classes**: Provide methods for specific API resources (Article, Project, Landing, SmartTable, etc.)
- **Error Handling System**: Provides detailed error messages and appropriate exception types
- **Configuration System**: Centralizes SDK settings and allows for customization

### Method Signature Design

All `create()` methods in the SDK follow a consistent pattern where required parameters are separated from optional ones for better clarity and IDE support. This design choice provides several benefits:

- **IDE Auto-completion**: Your IDE can suggest required parameters directly
- **Clear Requirements**: It's immediately obvious which parameters are mandatory
- **Better Documentation**: Required and optional parameters are clearly distinguished
- **Type Safety**: Required parameters are properly type-hinted

Example:
```python
# Clear separation of required and optional parameters
result = client.resource.create(
    required_param1="value1",  # Required
    required_param2="value2",  # Required
    additional_params={        # Optional
        "optional1": "value",
        "optional2": 123
    }
)
```

## 📚 Documentation

API documentation is available at [https://us.vsesvit.ai/api/v1/doc](https://us.vsesvit.ai/api/v1/doc).

## 📄 License

This SDK is distributed under the MIT license.

## 💬 Support

If you have any questions or issues, please create an Issue in this repository.

---

Created with ❤️ by the [Vsesvit AI](https://vsesvit.ai/) team | [Register](https://us.vsesvit.ai/en/register) | [Blog](https://vsesvit.ai/blog)