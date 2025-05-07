from typing import Optional, Dict, Any


class VsesvitAIError(Exception):
    """Base exception class for all VsesvitAI SDK errors."""

    def __init__(self, message: str = "An error occurred with the VsesvitAI API",
                 status_code: Optional[int] = None,
                 response_body: Optional[Dict[str, Any]] = None):
        self.status_code = status_code
        self.response_body = response_body or {}
        self.message = message
        super().__init__(self.message)


class AuthenticationError(VsesvitAIError):
    """Exception raised when there are problems with API authentication."""

    def __init__(self, message: str = "Invalid API key or credentials",
                 status_code: Optional[int] = 401,
                 response_body: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code, response_body)


class ResourceNotFoundError(VsesvitAIError):
    """Exception raised when the requested resource doesn't exist."""

    def __init__(self, resource_type: str = "resource",
                 resource_id: Optional[str] = None,
                 message: Optional[str] = None,
                 status_code: Optional[int] = 404,
                 response_body: Optional[Dict[str, Any]] = None):
        if message is None:
            message = f"The requested {resource_type} does not exist"
            if resource_id:
                message += f" (ID: {resource_id})"
        super().__init__(message, status_code, response_body)


class AccessDeniedError(VsesvitAIError):
    """Exception raised when access to a resource is denied."""

    def __init__(self, resource_type: str = "resource",
                 resource_id: Optional[str] = None,
                 message: Optional[str] = None,
                 status_code: Optional[int] = 401,
                 response_body: Optional[Dict[str, Any]] = None):
        if message is None:
            message = f"Access denied to this {resource_type}"
            if resource_id:
                message += f" (ID: {resource_id})"
        super().__init__(message, status_code, response_body)


class ValidationError(VsesvitAIError):
    """Exception raised when request data validation fails."""

    def __init__(self, message: str = "Request validation failed",
                 errors: Optional[Dict[str, Any]] = None,
                 status_code: Optional[int] = 400,
                 response_body: Optional[Dict[str, Any]] = None):
        self.errors = errors or {}
        if self.errors and not message.endswith(':'):
            message += ":"

        for field, error in self.errors.items():
            if isinstance(error, str):
                message += f"\n- {field}: {error}"
            elif isinstance(error, list) and error:
                message += f"\n- {field}: {', '.join(str(e) for e in error)}"

        super().__init__(message, status_code, response_body)


class RateLimitError(VsesvitAIError):
    """Exception raised when API rate limit is exceeded."""

    def __init__(self, message: str = "API rate limit exceeded",
                 retry_after: Optional[int] = None,
                 status_code: Optional[int] = 429,
                 response_body: Optional[Dict[str, Any]] = None):
        self.retry_after = retry_after
        if retry_after:
            message += f", retry after {retry_after} seconds"
        super().__init__(message, status_code, response_body)


class ServerError(VsesvitAIError):
    """Exception raised when the API server encounters an error."""

    def __init__(self, message: str = "API server error occurred",
                 status_code: Optional[int] = 500,
                 response_body: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code, response_body)


class NetworkError(VsesvitAIError):
    """Exception raised when network issues occur."""

    def __init__(self, message: str = "Network error occurred",
                 original_exception: Optional[Exception] = None):
        self.original_exception = original_exception
        if original_exception:
            message += f": {str(original_exception)}"
        super().__init__(message, None, None)
