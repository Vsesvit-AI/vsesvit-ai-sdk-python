import re
import requests
from typing import Tuple
from src.vsesvit_ai.config import SUPPORTED_RESOURCES, API_KEY_PREFIX, API_KEY_LENGTH
from src.vsesvit_ai.base.exceptions import *
from src.vsesvit_ai.errors.error_massages import *


def parse_resource_info(endpoint: str) -> Tuple[Optional[str], Optional[str]]:
    patterns = [
        r'^(?P<resource>\w+)/(?P<id>\d+)',
        r'^(?P<resource>\w+)/(?P<id>\d+)/\w+',
        r'^(?P<resource>\w+)'
    ]

    for pattern in patterns:
        match = re.match(pattern, endpoint)
        if match:
            groups = match.groupdict()

            resource_type = groups.get('resource', '')
            if resource_type.endswith('s'):
                resource_type = resource_type[:-1]

            return resource_type, groups.get('id')

    return None, None


def extract_error_info(response) -> tuple:
    """
    Extract error information from the response.

    :param response: Response object
    :return: Tuple of (error_message, response_body)
    """
    status_code = response.status_code

    try:
        response_body = response.json() if response.content else {}

        error_message = response_body.get('message', '')
        if not error_message:
            error_message = response_body.get('error', '')

        if not error_message and isinstance(response_body, dict):
            for key, value in response_body.items():
                if isinstance(value, dict) and 'message' in value:
                    error_message = value['message']
                    break
                elif isinstance(value, dict) and 'error' in value:
                    error_message = value['error']
                    break

        if not error_message:
            error_message = response.text[:100] or f"HTTP {status_code} error"

    except ValueError:
        response_body = {}
        error_message = response.text[:100] or f"HTTP {status_code} error"

    return error_message, response_body


def is_valid_api_key_format(api_key: str) -> bool:
    """
    Check if the API key matches the expected format.

    :param api_key: API key to check
    :return: True if the key format is valid
    """
    return api_key.startswith(API_KEY_PREFIX) and len(api_key) == API_KEY_LENGTH


def handle_error_response(
        response: requests.Response,
        endpoint: str,
        api_key: str,
        debug: bool = False) -> None:
    """
    Handle API error responses and raise appropriate exceptions.

    :param response: HTTP response object
    :param endpoint: The API endpoint that was called
    :param api_key: The API key used for the request
    :param debug: Whether to print debug information
    :raises: Appropriate VsesvitAIError subclass
    """
    status_code = response.status_code

    error_message, response_body = extract_error_info(response)

    if debug:
        print(f"Error Status Code: {status_code}")
        print(f"Error Message: {error_message}")
        print(f"Response Body: {response_body}")
        print(f"Endpoint: {endpoint}")
        print(f"Headers: {dict(response.headers)}")

    resource_type, resource_id = parse_resource_info(endpoint)

    if status_code == 401:
        if not is_valid_api_key_format(api_key):
            raise AuthenticationError(
                message=ERROR_INVALID_API_KEY,
                status_code=status_code,
                response_body=response_body
            )

        if resource_type in SUPPORTED_RESOURCES and resource_id:
            raise AccessDeniedError(
                resource_type=resource_type,
                resource_id=resource_id,
                message=ERROR_RESOURCE_ACCESS.format(resource=resource_type),
                status_code=status_code,
                response_body=response_body
            )

        raise AuthenticationError(
            message=ERROR_INVALID_API_KEY,
            status_code=status_code,
            response_body=response_body
        )

    elif status_code == 403:
        raise AccessDeniedError(
            resource_type=resource_type or "resource",
            resource_id=resource_id,
            message=error_message or ERROR_ACCESS_DENIED.format(resource=resource_type or "resource"),
            status_code=status_code,
            response_body=response_body
        )

    elif status_code == 404:

        message = ERROR_RESOURCE_NOT_FOUND.format(resource=resource_type or "resource")

        if resource_id:
            message += f" (ID: {resource_id})"

        raise ResourceNotFoundError(

            resource_type=resource_type or "resource",

            resource_id=resource_id,

            message=message,

            status_code=status_code,

            response_body=response_body

        )

    elif status_code == 400:
        validation_errors = response_body.get('errors', {})
        raise ValidationError(
            message=error_message or ERROR_VALIDATION_FAILED,
            errors=validation_errors,
            status_code=status_code,
            response_body=response_body
        )

    elif status_code == 429:
        retry_after = response.headers.get('Retry-After')
        if retry_after and retry_after.isdigit():
            retry_after = int(retry_after)
            message = ERROR_RATE_LIMIT_WITH_RETRY.format(retry=retry_after)
        else:
            retry_after = None
            message = ERROR_RATE_LIMIT

        raise RateLimitError(
            message=error_message or message,
            retry_after=retry_after,
            status_code=status_code,
            response_body=response_body
        )

    elif status_code >= 500:
        raise ServerError(
            message=error_message or ERROR_SERVER.format(status_code=status_code),
            status_code=status_code,
            response_body=response_body
        )

    else:
        raise VsesvitAIError(
            message=error_message or f"API error: HTTP {status_code}",
            status_code=status_code,
            response_body=response_body
        )
