# Error message templates
# These can be customized to change the error messages displayed to users

# Authentication errors
ERROR_INVALID_API_KEY = "Invalid API key or credentials"

# Resource access errors
ERROR_RESOURCE_ACCESS = "{resource} doesn't exist or you don't have permission to access it"
ERROR_ACCESS_DENIED = "Access denied to this {resource}"
ERROR_RESOURCE_NOT_FOUND = "The requested {resource} was not found"

# Validation errors
ERROR_VALIDATION_FAILED = "Validation failed"

# Rate limit errors
ERROR_RATE_LIMIT = "API rate limit exceeded"
ERROR_RATE_LIMIT_WITH_RETRY = "API rate limit exceeded, retry after {retry} seconds"

# Server errors
ERROR_SERVER = "Server error: HTTP {status_code}"

# Network errors
ERROR_NETWORK = "Network error connecting to VsesvitAI API: {error}"
