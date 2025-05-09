"""
Configuration settings for the VsesvitAI SDK.
These settings provide default values which can be overridden through environment variables.
"""
import os
from dotenv import load_dotenv

# Attempt to load .env file if it exists
# This won't cause an error if the file is missing
load_dotenv()

SUPPORTED_RESOURCES = [
    'article',
    'project',
    'landing',
    'knowledge_base',
    'user',
    'author',
    'audience',
    'smart_table'
]

# API key format settings
# The prefix that all valid API keys must start with
API_KEY_PREFIX = os.getenv('API_KEY_PREFIX', 'vsa_')
# The expected total length of a valid API key
API_KEY_LENGTH = int(os.getenv('API_KEY_LENGTH', '30'))

# Base URL for API requests
# Can be overridden for testing or using different environments
API_BASE_URL = os.getenv('API_BASE_URL', 'https://us.vsesvit.ai/api/v1')