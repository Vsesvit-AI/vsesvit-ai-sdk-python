from typing import Dict, Any


class User:
    def __init__(self, client):
        """
        Initialize the User resource

        :param client: VsesvitAI client instance
        """
        self.client = client

    def get_me(self) -> Dict[str, Any]:
        """
        Get information about the current authenticated user.

        :return: Dictionary with user profile information including id, email,
                 fullName, company, balance, and other user details
        :raises: AuthenticationError if API key is invalid
        :raises: AccessDeniedError if permission denied
        """
        return self.client.request("GET", "user/me")

    def get_referrals(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Returns a list of users who signed up using the current user's referral code.

        :param params: Query parameters for filtering and pagination
                      - offset: Number of items to skip (integer)
                      - limit: Number of items to return (integer)
                      - search: Search string to filter referrals by name (string)
        :return: Dictionary with referrals list and pagination info
        :raises: AuthenticationError if API key is invalid
        :raises: AccessDeniedError if permission denied
        :raises: ValidationError if query parameters are invalid
        """
        return self.client.request("GET", "user/referrals", params=params)